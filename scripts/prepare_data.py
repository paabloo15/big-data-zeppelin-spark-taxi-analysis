#!/usr/bin/env python3
"""Load, clean and enrich NYC Yellow Taxi parquet files using Spark."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    dayofweek,
    hour,
    to_date,
    unix_timestamp,
)

REQUIRED_COLUMNS = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount",
]


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description="Prepare NYC Yellow Taxi dataset using Spark."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=project_root / "data" / "raw",
        help="Directory with yellow_tripdata_YYYY-MM.parquet files.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=project_root / "data" / "processed" / "clean_taxi_trips.parquet",
        help="Output parquet path for cleaned dataset.",
    )
    parser.add_argument(
        "--summary-path",
        type=Path,
        default=project_root / "results" / "resumen_limpieza.csv",
        help="Output CSV path with cleaning summary.",
    )
    parser.add_argument(
        "--max-duration-minutes",
        type=float,
        default=240.0,
        help="Maximum allowed trip duration in minutes.",
    )
    parser.add_argument(
        "--max-speed-mph",
        type=float,
        default=80.0,
        help="Maximum allowed average speed in miles per hour.",
    )
    return parser.parse_args()


def validate_input_files(input_dir: Path) -> list[Path]:
    files = sorted(input_dir.glob("yellow_tripdata_*.parquet"))
    if not files:
        raise FileNotFoundError(
            f"No parquet files found in {input_dir}. Run download_data.py first."
        )
    return files


def validate_required_columns(columns: list[str]) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in columns]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Input data is missing required columns: {joined}")


def write_summary_csv(
    summary_path: Path,
    initial_rows: int,
    final_rows: int,
) -> None:
    removed_rows = initial_rows - final_rows
    removed_pct = (removed_rows / initial_rows * 100.0) if initial_rows else 0.0

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "registros_iniciales",
                "registros_finales",
                "registros_eliminados",
                "porcentaje_eliminado",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "registros_iniciales": initial_rows,
                "registros_finales": final_rows,
                "registros_eliminados": removed_rows,
                "porcentaje_eliminado": f"{removed_pct:.2f}",
            }
        )


def main() -> int:
    args = parse_args()

    try:
        input_files = validate_input_files(args.input_dir)
    except (FileNotFoundError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 1

    spark = (
        SparkSession.builder.appName("nyc_taxi_prepare_data")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )

    try:
        print("=== Reading raw parquet files ===")
        for file_path in input_files:
            print(f" - {file_path.name}")

        df_raw = spark.read.parquet(*[str(path) for path in input_files])

        validate_required_columns(df_raw.columns)

        print("\n=== Raw schema ===")
        df_raw.printSchema()

        initial_rows = df_raw.count()
        print(f"Initial rows: {initial_rows}")

        # Create reusable derived measures before filtering.
        df_enriched = (
            df_raw.withColumn(
                "trip_duration_minutes",
                (
                    unix_timestamp(col("tpep_dropoff_datetime"))
                    - unix_timestamp(col("tpep_pickup_datetime"))
                )
                / 60.0,
            )
            .withColumn(
                "average_speed_mph",
                col("trip_distance") / (col("trip_duration_minutes") / 60.0),
            )
        )

        # Filtering rules are explicit to keep cleaning traceable for defense.
        df_clean = (
            df_enriched.where(col("tpep_pickup_datetime").isNotNull())
            .where(col("tpep_dropoff_datetime").isNotNull())
            .where(col("trip_duration_minutes") > 0)
            .where(col("trip_duration_minutes") <= args.max_duration_minutes)
            .where(col("trip_distance") > 0)
            .where(col("fare_amount") >= 0)
            .where(col("tip_amount") >= 0)
            .where(col("total_amount") >= 0)
            .where(col("average_speed_mph") > 0)
            .where(col("average_speed_mph") <= args.max_speed_mph)
            .withColumn("pickup_date", to_date(col("tpep_pickup_datetime")))
            .withColumn("pickup_hour", hour(col("tpep_pickup_datetime")))
            .withColumn("pickup_day_of_week", dayofweek(col("tpep_pickup_datetime")))
        )

        final_rows = df_clean.count()
        removed_rows = initial_rows - final_rows
        removed_pct = (removed_rows / initial_rows * 100.0) if initial_rows else 0.0

        args.output_path.parent.mkdir(parents=True, exist_ok=True)
        df_clean.write.mode("overwrite").parquet(str(args.output_path))
        write_summary_csv(args.summary_path, initial_rows, final_rows)

        print("\n=== Cleaning summary ===")
        print(f"Final rows: {final_rows}")
        print(f"Removed rows: {removed_rows}")
        print(f"Removed percent: {removed_pct:.2f}%")
        print(f"Clean parquet saved to: {args.output_path}")
        print(f"Summary CSV saved to: {args.summary_path}")

        return 0

    except Exception as exc:  # pylint: disable=broad-except
        print(f"ERROR while preparing data: {exc}")
        return 1

    finally:
        spark.stop()


if __name__ == "__main__":
    sys.exit(main())
