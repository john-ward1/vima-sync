from datetime import datetime, timedelta
import pytz
import pandas as pd

APPLE_EPOCH = datetime(2001, 1, 1, tzinfo=pytz.UTC)

def normalize_runs(df: pd.DataFrame, timezone: str = "America/Los_Angeles") -> pd.DataFrame:
    tz = pytz.timezone(timezone)
    df = df.copy()

    df["start_utc"] = df["ZSTARTDATE"].apply(
        lambda x: APPLE_EPOCH + timedelta(seconds=x)
    )
    df["end_utc"] = df["ZENDDATE"].apply(
        lambda x: APPLE_EPOCH + timedelta(seconds=x)
    )

    df["start_local"] = df["start_utc"].dt.tz_convert(tz)
    df["end_local"] = df["end_utc"].dt.tz_convert(tz)

    df["duration_sec"] = df["ZENDDATE"] - df["ZSTARTDATE"]
    df["duration_min"] = df["duration_sec"] / 60

    df["distance_km"] = df["ZDISTANCE"] / 1000
    df["distance_miles"] = df["ZDISTANCE"] / 1609.34
    df["start_lat"] = df["ZLAT1"]
    df["start_lon"] = df["ZLONG1"]
    df["end_lat"] = df["ZLAT2"]
    df["end_lon"] = df["ZLONG2"]


    return df



