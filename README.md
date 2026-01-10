# vima-sync

Export your workout history from the **Vima Run iOS app** into standard formats for calendar integration.

## Features

- **CSV Export** – Analyze your runs in spreadsheets or data tools
- **Calendar Export (ICS)** – Import workouts into Apple Calendar or any calendar app
- **Local Processing** – No cloud sync, no credentials required
- **Privacy First** – All data stays on your machine

---

## Quick Start

If you already have the Vima database file (`RideTracker.sqlite`):

```bash
pip install vima-sync
cd path/to/RideTracker.sqlite
vima-sync --db RideTracker.sqlite --out .
```

**Outputs:**
- `vima_runs.csv` – All workout data in spreadsheet format
- `vima_runs.ics` – Calendar file ready to import

Double-click `vima_runs.ics` to import into Apple Calendar or drag it into your preferred calendar application.

---

## Installation

```bash
pip install vima-sync
```

**Requirements:**
- Python 3.7+
- iPhone backup (local or iCloud)

---

## Usage

### Basic Export

```bash
vima-sync --db RideTracker.sqlite --out .
```

### Disable Reverse Geocoding

For offline use or enhanced privacy (skips Nominatim API geolocation proceessing):

```bash
vima-sync --db RideTracker.sqlite --out . --no-geocode
```

---

## Getting the Database

Extracting `RideTracker.sqlite` from your iPhone backup is a **one-time setup**.

** See the full extraction guide:** [docs/EXTRACTION.md](docs/EXTRACTION.md)

---

## Privacy & Security

- **No jailbreaking required**
- **No private APIs**
- **Fully local processing**
- Reverse geocoding uses OpenStreetMap ([Nominatim](https://nominatim.org/)) when enabled
---

## License

MIT

---

## Disclaimer

This tool is not affiliated with or endorsed by Vima. Use at your own discretion.