import matplotlib.pyplot as plt
from pyfonts import load_google_font
from drawarrow import fig_arrow
import requests
from datetime import datetime
from collections import defaultdict
import pandas as pd
import mplcyberpunk


def get_weekly_downloads_df(package_name):
    url = f"https://pepy.tech/api/v2/projects/{package_name}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for {package_name}")

    data = response.json()
    daily_downloads = data["downloads"]

    weekly_downloads = defaultdict(int)

    for date_str, version_counts in daily_downloads.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        iso_year, iso_week, _ = date_obj.isocalendar()
        week_key = f"{iso_year}-W{iso_week:02d}"
        total_for_day = sum(version_counts.values())
        weekly_downloads[week_key] += total_for_day

    # Convert to DataFrame
    df = (
        pd.DataFrame(list(weekly_downloads.items()), columns=["week", "downloads"])
        .sort_values("week")
        .reset_index(drop=True)
    )

    return df


# Example usage
df_weekly = get_weekly_downloads_df("pyfonts")
df_weekly["week_start"] = pd.to_datetime(df_weekly["week"] + "-1", format="%G-W%V-%u")
df = df_weekly[df_weekly["week_start"] >= "2025-03-03"]
df = df.iloc[:-1]

plt.style.use("cyberpunk")
font = load_google_font("Roboto")
font_italic = load_google_font("Roboto", italic=True)

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(df["week_start"], df["downloads"], marker="o")

ax.yaxis.tick_right()
ax.set_ylim(0, 7000)
ax.set_xlim(right=pd.to_datetime("2025-05-07"))
ax.set_xticks(
    ["2025-03-05", "2025-04-05", "2025-05-05"],
    ["March 2025", "April 2025", "May 2025"],
    font=font,
)
ax.set_yticks(
    [i for i in range(1000, 6500, 1000)],
    labels=[i for i in range(1000, 6500, 1000)],
    font=font,
)
ax.tick_params(size=0, pad=5)
ax.grid(axis="y", color="#bfbfbf", zorder=-1, lw=0.4, alpha=0.2)
ax.grid(axis="x", alpha=0)

fig.text(
    x=0.1,
    y=0.76,
    s="Pyfonts is installed 1,000 times a day",
    size=20,
    font=font,
)
fig.text(
    x=0.23,
    y=0.65,
    s="(almost)",
    size=9,
    font=font,
)
fig_arrow(
    tail_position=[0.29, 0.655],
    head_position=[0.4, 0.75],
    color="lightgrey",
    mutation_scale=0.4,
    width=0.8,
    radius=0.3,
)

fig.text(
    x=0.73,
    y=0.93,
    s="Weekly downloads of PyFonts",
    size=8,
    color="#bfbfbf",
    font=font_italic,
)

mplcyberpunk.add_glow_effects()

fig.tight_layout()
fig.savefig("src/other/pyfonts-download/output.png", dpi=300, bbox_inches="tight")
