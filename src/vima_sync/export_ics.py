from ics import Calendar, Event

def export_ics(df, path: str):
    cal = Calendar()

    for _, r in df.iterrows():
        e = Event()
        e.name = f"Vima Run – {r['distance_miles']:.2f} mi"
        e.begin = r["start_local"]
        e.end = r["end_local"]

        # THIS is what Apple Calendar reads
        if r.get("location"):
            e.location = r["location"]

        e.description = (
            f"Distance: {r['distance_miles']:.2f} miles\n"
            f"Duration: {int(r['duration_min'])} minutes\n"
            f"Calories: {r['ZCALORIES']}\n\n"
            f"Start: {r['start_lat']}, {r['start_lon']}\n"
            f"End: {r['end_lat']}, {r['end_lon']}"
        )

        cal.events.add(e)

    with open(path, "w") as f:
        f.writelines(cal)

