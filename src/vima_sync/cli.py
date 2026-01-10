import argparse
from vima_sync.load import load_runs
from vima_sync.normalize import normalize_runs
from vima_sync.export_csv import export_csv
from vima_sync.export_ics import export_ics
from vima_sync.location import reverse_geocode


def main():
    parser = argparse.ArgumentParser(
        description="Export Vima Run data to CSV and ICS"
    )
    parser.add_argument(
        "--db",
        required=True,
        help="Path to RideTracker.sqlite"
    )
    parser.add_argument(
        "--out",
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--no-geocode",
        action="store_true",
        help="Disable reverse geocoding"
    )

    args = parser.parse_args()

    runs = load_runs(args.db)
    runs = normalize_runs(runs)

    if not args.no_geocode:
        runs["location"] = runs.apply(
            lambda r: reverse_geocode(r["start_lat"], r["start_lon"]),
            axis=1
        )
    else:
        runs["location"] = None

    export_csv(runs, f"{args.out}/vima_runs.csv")
    export_ics(runs, f"{args.out}/vima_runs.ics")

    print(f"Exported {len(runs)} runs")


if __name__ == "__main__":
    main()
