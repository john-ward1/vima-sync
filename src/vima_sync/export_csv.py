import pandas as pd

def export_csv(df, path: str):
    df[[
        "start_local",
        "end_local",
        "duration_min",
        "distance_miles",
        "ZCALORIES",
        "ZTOPSPEED",
        "start_lat",
        "start_lon",
        "end_lat",
        "end_lon"
    ]].to_csv(path, index=False)
