import pandas as pd
import matplotlib.pyplot as plt
from pypalettes import load_cmap
from pyfonts import load_google_font, set_default_font
import textwrap
from highlight_text import fig_text

url = "https://raw.githubusercontent.com/holtzy/the-python-graph-gallery/master/static/data/dataConsumerConfidence.csv"
df = pd.read_csv(url)

df = df.melt(id_vars=["Time"], var_name="country", value_name="value")
df["Time"] = pd.to_datetime(df["Time"], format="%b-%Y")
df = df.dropna()
df.head()


if "x" not in locals() or "x" not in globals():
    x = 0

colors = load_cmap("Antique").colors
bg_color = "#f4f4f9"
font = load_google_font("Bricolage Grotesque")
font_bold = load_google_font("Bricolage Grotesque", weight="bold")
set_default_font(font)

fig, axs = plt.subplots(nrows=3, ncols=3)
axs = axs.flatten()

fig.set_facecolor(bg_color)

for i, (country, ax) in enumerate(zip(df["country"].unique(), axs)):
    main_df = df[df["country"] == country]
    other_df = df[df["country"] != country]
    sorted_df = main_df.sort_values(by="Time")
    last_value = sorted_df.iloc[-1]["value"]
    last_date = sorted_df.iloc[-1]["Time"]

    # main line
    ax.plot(
        main_df["Time"], main_df["value"], zorder=10, clip_on=False, color=colors[i]
    )
    ax.plot(
        last_date,
        last_value,
        marker="o",
        markersize=5,
        color=colors[i],
    )
    ax.text(
        last_date,
        last_value * 1.007,
        f"{round(last_value)}",
        fontsize=7,
        color=colors[i],
        font=font_bold,
    )

    # other lines
    for other_country in other_df["country"].unique():
        other_sub_df = other_df[other_df["country"] == other_country]
        ax.plot(
            other_sub_df["Time"],
            other_sub_df["value"],
            color="black",
            zorder=5,
            alpha=0.1,
            clip_on=False,
        )

    ax.set_facecolor(bg_color)
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.set_xticks([])
    ax.tick_params(axis="y", size=0)
    ax.set_ylim(91, 105)
    ax.hlines(
        y=100,
        xmin=0,
        xmax=1,
        transform=ax.get_yaxis_transform(),
        colors="black",
        linewidth=0.6,
        alpha=0.8,
    )
    ax.text(
        x=0.1,
        y=1.1,
        s=f"{country.title()}",
        font=font_bold,
        size=8,
        transform=ax.transAxes,
    )

    if i in [0, 3, 6]:
        ax.set_yticks([100])
    else:
        ax.set_yticks([])

fig.text(
    x=0.5,
    y=1.18,
    s="Consumer Confidence Around the World",
    font=font_bold,
    size=18,
    ha="center",
    va="top",
)

description = """
    The consumer confidence indicator provided an indication of future developments of households consumption and saving. An indicator above 100 signals a boost in the consumers' confidence towards the future economic situation. Values below 100 indicate a pessimistic attitude towards future developments in the economy, possibly resulting in a tendency to save more and consume less. During 2022, the consumer confidence indicators have declined in many major economies around the world.
"""
description_filled = textwrap.fill(description, width=90)
fig.text(
    x=0.5,
    y=1.11,
    s=description_filled,
    color="#2f4550",
    size=8,
    ha="center",
    va="top",
)

source_params = dict(
    va="top", color="darkgrey", size=7, highlight_textprops=[{"font": font_bold}]
)
fig_text(x=0.1, y=0.09, s="<Original chart>: Gilbert Fontana", **source_params)
fig_text(x=0.1, y=0.06, s="<Data>: OECD, 2022", **source_params)

x += 1
plt.savefig(f"src/other/sandbox/temp/{x}.png", dpi=300, bbox_inches="tight")
plt.savefig("cache.png", dpi=300, bbox_inches="tight")
