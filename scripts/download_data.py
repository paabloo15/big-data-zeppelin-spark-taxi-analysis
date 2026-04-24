#!/usr/bin/env python3
"""Download Yellow Taxi parquet files from NYC TLC public endpoint."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
FILENAME_TEMPLATE = "yellow_tripdata_{year}-{month:02d}.parquet"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Yellow Taxi parquet files from NYC TLC."
    )
    parser.add_argument(
        "--year",
        type=int,
        required=True,
        help="Year to download (example: 2023).",
    )
    parser.add_argument(
        "--months",
        type=int,
        nargs="+",
        required=True,
        help="One or more month numbers (1-12). Example: --months 1 2 3",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "raw",
        help="Destination folder for parquet files.",
    )
    return parser.parse_args()


def validate_months(months: list[int]) -> list[int]:
    normalized = sorted(set(months))
    invalid = [month for month in normalized if month < 1 or month > 12]
    if invalid:
        values = ", ".join(str(value) for value in invalid)
        raise ValueError(f"Invalid month values: {values}. Allowed range is 1..12.")
    return normalized


def download_file(url: str, destination: Path) -> tuple[bool, str]:
    if destination.exists() and destination.stat().st_size > 0:
        return False, f"SKIP: file already exists -> {destination.name}"

    try:
        urllib.request.urlretrieve(url, destination)
        return True, f"OK: downloaded -> {destination.name}"
    except urllib.error.HTTPError as exc:
        if destination.exists():
            destination.unlink()
        return False, f"ERROR HTTP {exc.code} for {destination.name}: {exc.reason}"
    except urllib.error.URLError as exc:
        if destination.exists():
            destination.unlink()
        return False, f"ERROR NETWORK for {destination.name}: {exc.reason}"
    except OSError as exc:
        if destination.exists():
            destination.unlink()
        return False, f"ERROR FILESYSTEM for {destination.name}: {exc}"


def main() -> int:
    args = parse_args()

    try:
        months = validate_months(args.months)
    except ValueError as exc:
        print(str(exc))
        return 2

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== NYC TLC Yellow Taxi Downloader ===")
    print(f"Year: {args.year}")
    print(f"Months: {months}")
    print(f"Output directory: {output_dir}")

    downloaded_count = 0
    skipped_count = 0
    error_count = 0

    for month in months:
        filename = FILENAME_TEMPLATE.format(year=args.year, month=month)
        url = f"{BASE_URL}/{filename}"
        destination = output_dir / filename

        print(f"\nDownloading {filename} ...")
        ok, message = download_file(url, destination)
        print(message)

        if message.startswith("SKIP"):
            skipped_count += 1
        elif ok:
            downloaded_count += 1
        else:
            error_count += 1

    print("\n=== Summary ===")
    print(f"Downloaded: {downloaded_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")

    if error_count > 0:
        print("Some files were not downloaded. Check messages above.")
        return 1

    print("Download process completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
