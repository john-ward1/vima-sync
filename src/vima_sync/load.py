import sqlite3
import pandas as pd

def load_runs(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("""
        SELECT
            Z_PK,
            ZSTARTDATE,
            ZENDDATE,
            ZDISTANCE,
            ZCALORIES,
            ZTOPSPEED,
            ZLAT1,
            ZLONG1,
            ZLAT2,
            ZLONG2,
            ZTYPE
        FROM ZTRACK
        WHERE ZTYPE = 'Run'
        ORDER BY ZSTARTDATE
    """, conn)
    conn.close()
    return df


def load_gps_points(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("""
        SELECT
            ZALTITUDE,
            ZLATITUDE,
            ZLONGITUDE,
            ZSPEED,
            ZFILENAME
        FROM ZGPSPOINT
        ORDER BY ZFILENAME
    """, conn)
    conn.close()
    return df
