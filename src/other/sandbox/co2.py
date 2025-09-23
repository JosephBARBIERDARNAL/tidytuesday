import pandas as pd
import os
import matplotlib.pyplot as plt
from pyfonts import load_google_font
from gifing import GIF


url = "https://raw.githubusercontent.com/holtzy/the-python-graph-gallery/master/static/data/data-CO2.csv"
df = pd.read_csv(url)


def circle_countries(country_names: list):
    df["EdgeColor"] = df["Color"]
    df.loc[df["Name"].isin(country_names), "EdgeColor"] = "black"
    return df["EdgeColor"]


def add_country_name(country_names: list):
    for country_name in country_names:
        x_axis = df.loc[df["Name"] == country_name, "&nbsp;"]
        y_axis = df.loc[df["Name"] == country_name, "&nbsp;.1"]
        ax.text(
            x_axis,
            y_axis + 0.03,  # position
            country_name,  # label
            size=6,  # size of the text
            ha="center",  # align the text
        )


font_bold = load_google_font("Roboto", weight="bold")
font_regular = load_google_font("Roboto")

country_to_circle = [
    "Norway",
    "Singapore",
    "U.S.",
    "Czech Republic",
    "Qatar",
    "Bahrain",
    "Somalia",
    "Sudan",
    "India",
    "Trinidad and Tobago",
    "Chad",
]
edgecolors = circle_countries(country_to_circle)

# x = 0

fig, ax = plt.subplots()

ax.scatter(
    df["&nbsp;"],
    df["&nbsp;.1"],
    s=df["CO2 per Capita"] * 10,
    c=df["Color"],
    marker="s",
    edgecolor="none",
    zorder=2,
)

# overlay highlighted countries
highlight_df = df[df["Name"].isin(country_to_circle)]
ax.scatter(
    highlight_df["&nbsp;"],
    highlight_df["&nbsp;.1"],
    s=highlight_df["CO2 per Capita"] * 10,
    c=highlight_df["Color"],
    marker="s",
    edgecolor="black",
    linewidth=0.8,
    zorder=3,  # higher than base
)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
fig.text(0.1, 0.45, "High readiness", color="silver", size=8)
fig.text(0.1, 0.4, "Low readiness", color="silver", size=8)

line_args = dict(color="gray", linestyle="--", linewidth=0.7, alpha=0.4)
ax.axvline(0.43, **line_args)
ax.axhline(0.41, **line_args)

add_country_name(country_to_circle)

arrowprops = dict(arrowstyle="->", color="silver", lw=0.4)
ax.annotate("", xy=(0.25, 0.32), xytext=(0.25, 0.37), arrowprops=arrowprops)
ax.annotate("", xy=(0.25, 0.5), xytext=(0.25, 0.45), arrowprops=arrowprops)


title = "The countries with the highest vulnerability to climate change\nhave the lowest CO2 emissions"
fig.text(
    0.05,
    0.97,
    title,
    fontsize=11,
    ha="left",
    font=font_bold,
)
subtitle = "All countries sorted by their vulnerability and readiness to climate change. The size shows the CO2 emission\nper person in that country"
fig.text(
    0.05,
    0.9,
    subtitle,
    fontsize=8,
    ha="left",
    multialignment="left",
    font=font_regular,
)

# x += 1
# fig.savefig(f"src/other/sandbox/temp/{x}.png", bbox_inches="tight", dpi=200)


dir_path = "src/other/sandbox/temp/"
files = sorted(os.listdir(dir_path), key=lambda x: int(x.split(".")[0]))
files = [os.path.join(dir_path, f) for f in files]
gif = GIF(file_path=files, frame_duration=250, n_repeat_last_frame=10)
gif.set_size((1500, 1500))
gif.set_background_color("white")
gif.make("src/other/sandbox/evolution.gif")
