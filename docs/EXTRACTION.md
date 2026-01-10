# vima-sync

Export your workout history from the **Vima Run iOS app** into:
- CSV (for analysis / backup)
- Calendar ICS format

All processing is **local**. No cloud sync. No credentials.

---

## What this does

`vima-sync` takes the SQLite database used by the Vima Run app and:

- Normalizes timestamps and units
- Converts distances to miles
- Converts durations to minutes
- Adds a human-readable location (optional)
- Exports:
  - `vima_runs.csv`
  - `vima_runs.ics`

---

## Prerequisites

- macOS
- Python 3.10+
- A local iPhone backup that contains Vima Run data

---

## Step 1 — Back up your iPhone locally

1. Plug your iPhone into your Mac
2. Open **Finder**
3. Select your iPhone
4. Click **Back Up Now**
5. It will prompt you for a password to encrypt the local backup, note this backup password. I refer to it as "YOUR_NEW_BACKUP_PASSWORD".

This creates a local backup under:
```
~/Library/Application Support/MobileSync/Backup/
```
6. To get this backup, go to finder, "Go", then hold down the "Option" key to display the "Library" folder, click on "Application Support", then "MobileSync", then "Backup", then click on the folder. Its going to be numbered file, that has numerous folders that are useless unless you decrypt it.

<img width="400" height="415" alt="Screenshot 2026-01-10 at 10 27 00 AM" src="https://github.com/user-attachments/assets/4bd88c86-956e-4f39-9a74-6fa3862ec7c7" />

7. You'll now need to decrypt the local backup to make sense of the data.  To do that, create a python script in terminal, which requires the iphone_backup_decrypt library.

```
python -m pip install iphone_backup_decrypt
```
Then create a python script in terminal with:
```
nano decrypt_backup.py
```
Paste
```

from iphone_backup_decrypt.iphone_backup import EncryptedBackup
from iphone_backup_decrypt import DomainLike
import os
import shutil

backup_dir = "/Users/<YOUR_USERNAME>/Library/Application Support/MobileSync/Backup/00008030-00125C2E0287C02E"
out_dir = "/Users/<YOUR_USERNAME>/vima_extracted"

# clean output
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)

backup = EncryptedBackup(
    backup_directory=backup_dir,
    passphrase="YOUR_NEW_BACKUP_PASSWORD"
)

backup.test_decryption()

# extract ONLY the Vima app sandbox
backup.extract_files(
    domain_like="AppDomain-com.vima%",
    output_folder=out_dir,
    preserve_folders=True,
    domain_subfolders=True
)

print("DONE")
```
Then Run 
```
python decrypt_backup.py
```
This creates a folder that extracted the AppDomain-com.dc.Vima folder from the local backup.  Search for a file named "vima_extracted". 
Optionally, you can list all the folders from your local backup decrypted through running this command. I initially used it to verify which specific domain (ie "AppDomain-com.vima") the Vima files could be found to reference in the decrypt_backup.py script.
```
nano list.py
```
```
from iphone_backup_decrypt.iphone_backup import EncryptedBackup

backup_dir = "/Users/<YOUR_USERNAME>/Library/Application Support/MobileSync/Backup/00008030-00125C2E0287C02E"

backup = EncryptedBackup(
    backup_directory=backup_dir,
    passphrase="YOUR_NEW_BACKUP_PASSWORD"
)

backup.test_decryption()

with backup.manifest_db_cursor() as cur:
    cur.execute("SELECT DISTINCT domain FROM Files ORDER BY domain;")
    domains = cur.fetchall()

for d in domains:
    print(d[0])
```

Inside the "vima_extracted" folder, this RideTracker.sqlite database is what you're looking for. It is the db that the Vima applications uses to store run data on your phone.  

<img width="221" height="195" alt="Screenshot 2026-01-10 at 9 09 23 AM" src="https://github.com/user-attachments/assets/905ef548-e15d-466b-a678-956500b76de6" />


Open it with a database application.

<img width="500" height="300" alt="Screenshot 2025-12-30 at 2 23 24 PM" src="https://github.com/user-attachments/assets/71440240-2dd3-495c-8055-3feb59893252" />

---

Now navigate to the folder that holds the RideTracker.sqlite. In this case it would be: 

```
cd ~/vima_extracted/AppDomain-com.dc.Vima/Documents
```

---

## Step 3 — Install vima-sync

```bash
pip install vima-sync
```

Or for development:

```bash
git clone https://github.com/john-ward1/vima-sync.git
cd vima-sync
pip install -e .
```

---

## Step 4 — Run the command

Run `vima-sync`, pointing it at the extracted Vima database 
```bash
vima-sync --db RideTracker.sqlite --out .
```

This creates the following files in the output directory:
- `vima_runs.csv`
- `vima_runs.ics`

<img width="240" height="264" alt="Screenshot 2026-01-10 at 9 37 29 AM" src="https://github.com/user-attachments/assets/b881097e-2112-4522-b0a9-523e49ee2a27" />

---

Your runs will appear as calendar events. with the distance, duration, calories, location (start and end coordinates)

---

## Options

### Disable reverse geocoding

If you want to disable converting coordinates into a human-readable location:

```bash
vima-sync --db RideTracker.sqlite --out . --no-geocode
```

---

## Output details

### CSV (vima_runs.csv)

- One row per run
- Normalized units (miles, minutes)
- Start and end coordinates
- Human-readable location string

Ready for:
- Microsoft Excel
- Google Sheets
- Pandas
- BI / analytics tools

### Calendar (vima_runs.ics)

- Event title shows distance in miles
- Description includes:
  - Duration (minutes)
  - Calories
  - Coordinates
- Location field populated with a place name
- Compatible with Apple Calendar and Google Calendar

---

## Notes

- This project does not jailbreak your phone
- It does not access private or undocumented APIs
- All processing happens locally on your machine
- Reverse geocoding uses OpenStreetMap (Nominatim)
