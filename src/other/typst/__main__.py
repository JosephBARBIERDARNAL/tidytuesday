import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pyfonts import load_google_font, set_default_font
from highlight_text import fig_text
from drawarrow import fig_arrow
import polars as pl

set_default_font(load_google_font("Hanken Grotesk"))
bold = load_google_font("Hanken Grotesk", weight="bold")

df = pl.read_csv("src/other/typst/typst.csv").with_columns(
    pl.col("Date")
    .str.replace(r" \(.*\)", "")  # Remove timezone name in parentheses
    .str.replace("GMT", "")  # Remove GMT prefix
    .str.strptime(pl.Datetime, "%a %b %d %Y %H:%M:%S %z")
    .alias("Date")
)
xmin, xmax = df.select(
    pl.col("Date").min().alias("xmin"),
    pl.col("Date").max().alias("xmax"),
).row(0)


fig, ax = plt.subplots(figsize=(11, 5))

ax.spines[["top", "right", "left"]].set_visible(False)
ax.hlines(
    y=[i * 1000 for i in range(0, 51, 10)],
    xmin=xmin,
    xmax=xmax,
    color="black",
    linewidth=1,
    alpha=0.1,
)
ax.set_yticks(
    [i * 1000 for i in range(10, 51, 10)],
    labels=[f"{i}k" for i in range(10, 51, 10)],
)
ax.set_ylim(0, 52000)
ax.tick_params(pad=4)
ax.tick_params(axis="y", pad=-15, length=0)
ax.fill_between(df["Date"].to_list(), df["Stars"].to_list(), alpha=0.4, color="#1a7a87")
ax.plot(df["Date"].to_list(), df["Stars"].to_list(), color="#239dad", linewidth=2)
ax.scatter(
    df["Date"].to_list(),
    df["Stars"].to_list(),
    color="#239dad",
    s=50,
    clip_on=False,
    zorder=20,
)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
for year in (2024, 2025, 2026):
    jan = datetime(year, 1, 1, tzinfo=xmin.tzinfo)
    ax.text(
        jan,
        -0.08,  # vertical offset below ticks
        str(year),
        transform=ax.get_xaxis_transform(),
        font=bold,
        ha="center",
        va="top",
    )

# Annotations for specific data points
annotations = [
    (datetime(2023, 7, 19, tzinfo=xmin.tzinfo), 18500, "18.5k"),
    (datetime(2024, 1, 9, tzinfo=xmin.tzinfo), 23800, "23.8k"),
    (datetime(2024, 9, 9, tzinfo=xmin.tzinfo), 31800, "31.8k"),
    (datetime(2025, 5, 14, tzinfo=xmin.tzinfo), 39800, "39.8k"),
]
for date, value, label in annotations:
    ax.vlines(date, 0, value, color="black", linewidth=1, linestyle="-", alpha=0.5)
    ax.text(date, value + 1500, label, ha="center", va="bottom", size=8, font=bold)

fig.text(
    x=0.6,
    y=0.78,
    s="+51k stars in 2026!",
    size=8.5,
    ha="center",
    font=bold,
)
fig_arrow([0.65, 0.81], [0.85, 0.87], radius=-0.1, color="black")

fig_text(
    x=0.5,
    y=0.96,
    s="Total number of <stars> in the <Typst> GitHub repository",
    size=20,
    ha="center",
    highlight_textprops=[{"font": bold}, {"color": "#1a7a87", "font": bold}],
)

plt.savefig("src/other/typst/output.png", dpi=300, bbox_inches="tight")
