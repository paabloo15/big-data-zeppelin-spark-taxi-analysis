#!/usr/bin/env python3
"""Run simple didactic benchmark queries on Parquet and CSV datasets."""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description="Benchmark simple analytical queries on Parquet and CSV."
    )
    parser.add_argument(
        "--parquet-path",
        type=Path,
        default=project_root / "data" / "processed" / "clean_taxi_trips.parquet",
        help="Path to cleaned parquet dataset.",
    )
    parser.add_argument(
        "--csv-path",
        type=Path,
        default=project_root / "data" / "processed" / "sample_taxi_trips.csv",
        help="Path to CSV sample dataset.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=project_root / "results" / "metricas_consultas.csv",
        help="Output CSV path for benchmark metrics.",
    )
    return parser.parse_args()


def normalize_columns(df: DataFrame) -> DataFrame:
    return (
        df.select(
            F.col("pickup_hour").cast("int").alias("pickup_hour"),
            F.col("fare_amount").cast("double").alias("fare_amount"),
            F.col("trip_duration_minutes").cast("double").alias("trip_duration_minutes"),
        )
        .where(F.col("pickup_hour").isNotNull())
        .where(F.col("fare_amount").isNotNull())
        .where(F.col("trip_duration_minutes").isNotNull())
    )


def run_timed_query(df: DataFrame, query_name: str) -> tuple[float, int]:
    start = time.perf_counter()

    if query_name == "numero_total_viajes":
        result = df.select(F.count(F.lit(1)).alias("total_viajes"))
    elif query_name == "viajes_por_hora":
        result = df.groupBy("pickup_hour").agg(F.count(F.lit(1)).alias("total_viajes")).orderBy(
            "pickup_hour"
        )
    elif query_name == "tarifa_media_por_hora":
        result = df.groupBy("pickup_hour").agg(F.avg("fare_amount").alias("fare_media")).orderBy(
            "pickup_hour"
        )
    elif query_name == "duracion_media_por_hora":
        result = (
            df.groupBy("pickup_hour")
            .agg(F.avg("trip_duration_minutes").alias("duracion_media_min"))
            .orderBy("pickup_hour")
        )
    else:
        raise ValueError(f"Unknown query name: {query_name}")

    output_rows = result.count()
    elapsed = time.perf_counter() - start
    return elapsed, output_rows


def write_metrics(output_path: Path, rows: list[dict[str, str]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "formato",
                "consulta",
                "segundos",
                "filas_entrada",
                "filas_salida",
                "nota",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()

    if not args.parquet_path.exists():
        print(f"ERROR: parquet dataset not found: {args.parquet_path}")
        print("Run prepare_data.py first.")
        return 1

    if not args.csv_path.exists():
        print(f"ERROR: CSV sample not found: {args.csv_path}")
        print("Run convert_sample_to_csv.py first.")
        return 1

    spark = SparkSession.builder.appName("nyc_taxi_benchmark_queries").getOrCreate()

    try:
        print(f"Reading parquet: {args.parquet_path}")
        parquet_df = normalize_columns(spark.read.parquet(str(args.parquet_path)))

        print(f"Reading csv: {args.csv_path}")
        csv_df = normalize_columns(
            spark.read.option("header", True).option("inferSchema", True).csv(str(args.csv_path))
        )

        parquet_rows = parquet_df.count()
        csv_rows = csv_df.count()
        base_rows = min(parquet_rows, csv_rows)

        if base_rows == 0:
            print("ERROR: one dataset has zero rows after normalization.")
            return 1

        print(f"Rows parquet (normalized): {parquet_rows}")
        print(f"Rows csv (normalized): {csv_rows}")
        print(f"Rows used for fair comparison: {base_rows}")

        parquet_base = parquet_df.limit(base_rows).cache()
        csv_base = csv_df.limit(base_rows).cache()

        # Materialize cache to reduce startup noise in query timings.
        parquet_base.count()
        csv_base.count()

        query_names = [
            "numero_total_viajes",
            "viajes_por_hora",
            "tarifa_media_por_hora",
            "duracion_media_por_hora",
        ]

        metric_rows: list[dict[str, str]] = []

        for dataset_name, dataset_df in (("parquet", parquet_base), ("csv", csv_base)):
            for query_name in query_names:
                elapsed, output_rows = run_timed_query(dataset_df, query_name)
                metric_rows.append(
                    {
                        "formato": dataset_name,
                        "consulta": query_name,
                        "segundos": f"{elapsed:.4f}",
                        "filas_entrada": str(base_rows),
                        "filas_salida": str(output_rows),
                        "nota": "comparativa didactica, no benchmark cientifico",
                    }
                )
                print(
                    f"{dataset_name} | {query_name} -> {elapsed:.4f}s "
                    f"(output rows: {output_rows})"
                )

        write_metrics(args.output_path, metric_rows)
        print(f"Benchmark metrics saved to: {args.output_path}")
        return 0

    except Exception as exc:  # pylint: disable=broad-except
        print(f"ERROR while running benchmark: {exc}")
        return 1

    finally:
        spark.stop()


if __name__ == "__main__":
    sys.exit(main())
