from drawarrow import ax_arrow
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pypalettes import create_cmap
from pyfonts import load_google_font


df = pd.read_csv("src/other/co2-country/co2_emissions_2022.csv")
df.head()

gdf = gpd.read_file("src/other/co2-country/europe.geojson").merge(
    df, right_on="Country", left_on="NAME"
)[
    [
        "Country",
        "geometry",
        "CO2_Emissions_tons_2022",
        "Year_Change_percent",
        "Population_2022",
        "Per_Capita_tons",
        "Share_of_World_percent",
    ]
]
gdf_projected = gdf.to_crs(epsg=3035)
gdf_projected["centroid"] = gdf_projected.geometry.centroid
gdf["centroid"] = gdf_projected["centroid"].to_crs(gdf.crs)
gdf.head()

cmap = create_cmap(
    [
        "#22394A",
        "#244E57",
        "#368990",
        "#6FC0BA",
        "#F4C659",
        "#D9792E",
        "#AF2213",
        "#871C0F",
    ],
    cmap_type="continuous",
)
bg_color = "#fefae0"
font_country = load_google_font("Momo Trust Display")

fig, ax = plt.subplots(figsize=(5, 5))
fig.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

col = "Year_Change_percent"
gdf.plot(
    ax=ax,
    column=col,
    cmap=cmap,
    lw=0,
    vmin=-27,
    vmax=27,
)

ax.axis("off")
ax.set_xlim(-25, 52)
ax.set_ylim(34, 72)

adjustments = {
    "Italy": (-2, 2.5),
    "Finland": (0, -2),
    "Belarus": (0, -0.4),
    "Germany": (-0.2, 0),
    "Iceland": (0, -0.3),
    "Ukraine": (0, 0.5),
    "Luxembourg": (-3, 5),
}
country_to_annotate = [
    "France",
    "Spain",
    "Turkey",
    "Russia",
    "Germany",
    "Poland",
    "Ukraine",
    "Romania",
    "Italy",
    "Luxembourg",
    "Belarus",
    "Iceland",
    "Finland",
]
# country_to_annotate = gdf.Country.unique()
for country in country_to_annotate:
    centroid = gdf.loc[gdf["Country"] == country, "centroid"].values[0]
    x_val, y_val = centroid.coords[0]
    try:
        x_val += adjustments[country][0]
        y_val += adjustments[country][1]
    except KeyError:
        pass
    value = gdf.loc[gdf["Country"] == country, col].values[0]
    if abs(value) > 15:
        text_color = "white"
    else:
        text_color = "black"
    if value > 0:
        txt_add = "+"
    else:
        txt_add = ""
    ax.text(
        x=x_val,
        y=y_val,
        s=f"{country}\n{txt_add}{value:.1f}%",
        color=text_color,
        fontsize=3.5,
        font=font_country,
        ha="center",
        va="center",
    )

ax_arrow(
    [3, 54],
    [5.8, 49.7],
    color="black",
    head_length=2,
    head_width=1,
    width=0.4,
    radius=0.2,
)

fig.text(
    x=0.15,
    y=0.8,
    s="Change in CO2 emissions\nbetween 2022 and 2021",
    font=font_country,
    size=10,
    va="top",
)
fig.text(
    x=0.15,
    y=0.22,
    s="CO2 Emissions by Country - Worldometer\nGraphic by Joseph Barbier",
    font=font_country,
    color="#6c757d",
    size=3,
    va="top",
)

plt.savefig("src/other/co2-country/output.png", dpi=300, bbox_inches="tight")
