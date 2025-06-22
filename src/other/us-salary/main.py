import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from matplotlib import font_manager
from pyfonts import load_google_font
from pypalettes import load_cmap


def set_font(family):
    font = load_google_font(family)
    font_file = font.get_file()
    font_manager.fontManager.addfont(font_file)
    plt.rcParams["font.family"] = family


# x = 0

df_salary = pd.read_csv("src/other/us-salary/salary.csv")
gdf = gpd.read_file("src/other/us-salary/us.geojson").merge(df_salary, on="state")
gdf = gdf[gdf["salary"] < 100]  # remove district of columbia
gdf = gdf[gdf["state"] != "Alaska"]
gdf = gdf[gdf["state"] != "Hawaii"]

gdf_projected = gdf.to_crs(epsg=3035)
gdf_projected["centroid"] = gdf_projected.geometry.centroid
gdf["centroid"] = gdf_projected["centroid"].to_crs(gdf.crs)

set_font("Roboto")
font1 = load_google_font("Ubuntu", italic=True)
font2 = load_google_font("Ubuntu")
cmap = load_cmap("enara", cmap_type="continuous", reverse=True)
ec = "white"
lw = 0
text_color = "white"

fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

gdf.plot(ax=ax, column="salary", cmap=cmap, ec=ec, lw=lw)

ax.set_xlim(-130, -65)
ax.set_ylim(20, 50)
ax.axis("off")

bar_ax = ax.inset_axes(bounds=[0.05, -0.05, 0.5, 0.4], zorder=-1)
n, bins, _ = bar_ax.hist(gdf["salary"], bins=15, alpha=0)
colors = [cmap((val - min(bins)) / (max(bins) - min(bins))) for val in bins]
bar_ax.bar(bins[:-1], n, color=colors, width=2, ec=ec, lw=lw)
bar_ax.spines[["top", "left", "right"]].set_visible(False)
bar_ax.set_yticks([])
x_ticks = list(range(50, 90, 10))
x_tick_labels = [f"{val}k" for val in x_ticks]
bar_ax.set_xticks(x_ticks, labels=x_tick_labels, size=8)
bar_ax.tick_params(axis="x", length=0, pad=5)

exclude = {
    "Indiana",
    "Michigan",
    "Mississippi",
    "Florida",
    "New Jersey",
    "West Virginia",
    "South Carolina",
    "Louisiana",
    "Massachusetts",
    "Vermont",
    "Connecticut",
    "Maryland",
    "Delaware",
    "Rhode Island",
    "New Hampshire",
}
states_to_annotate = [state for state in gdf.state.to_list() if state not in exclude]

adjustments = {
    "California": (0, -1),
    "Kentucky": (0, -0.2),
    "Washington": (0.5, -0.4),
    "Virginia": (0, -0.2),
    "Idaho": (0, -0.4),
    "New York": (0, -0.2),
}

for state in states_to_annotate:
    centroid = gdf.loc[gdf["state"] == state, "centroid"].values[0]
    x_val, y_val = centroid.coords[0]
    try:
        x_val += adjustments[state][0]
        y_val += adjustments[state][1]
    except KeyError:
        pass
    value = gdf.loc[gdf["state"] == state, "salary"].values[0]
    if value <= 65:
        color_text = "black"
    else:
        color_text = text_color
    ax.text(
        x=x_val,
        y=y_val,
        s=f"{state.upper()}\n${value:.0f}k",
        fontsize=5,
        font=font2,
        color=color_text,
        ha="center",
        va="center",
    )

fig.text(
    x=0.5,
    y=0.8,
    s="Average salary in the United States in 2025",
    ha="center",
    size=22,
    font=load_google_font("Roboto Slab"),
)

credit_params = dict(x=0.9, ha="right", size=7, font=font1, va="bottom")
fig.text(y=0.24, s="Graphic: Joseph Barbier", **credit_params)
fig.text(y=0.22, s="Data from Forbes and the U.S. Census Bureau", **credit_params)
fig.text(y=0.2, s="Data do not include District of Columbia", **credit_params)

fig.tight_layout()

x += 1
fig.savefig(f"src/other/us-salary/temp/{x}.png", dpi=300, bbox_inches="tight")
