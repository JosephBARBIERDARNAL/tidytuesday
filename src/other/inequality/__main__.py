import polars as pl
from polars import col
import matplotlib.pyplot as plt
from pypalettes import load_cmap
from pyfonts import load_google_font
from dateutil.relativedelta import relativedelta


font_bold = load_google_font("Staatliches")
font_regular = load_google_font("Raleway", weight=700)
font_italic = load_google_font("Raleway", weight=400, italic=True)

colors = load_cmap("Classic_10_Light").colors
bg_color = "#222725"

countries = [
    "Australia",
    "Sweden",
    "China",
    "France",
    "Japan",
    "South Africa",
    "South Korea",
    "Taiwan",
    "United States",
]

df = (
    pl.read_csv("src/other/inequality/gini-coefficient.csv")
    .filter(col("Country").is_in(countries))
    .with_columns(
        Year=col("Year").cast(pl.String).str.to_date(format="%Y").cast(pl.Date)
    )
    .filter(col("Year") >= 1980)
    .sort(["Country", "Year"])
    .with_columns(col("Gini").interpolate().over("Country"))
)
df.head()


fig, axs = plt.subplots(nrows=3, ncols=3, sharex=True, sharey=True, figsize=(10, 6))
fig.set_facecolor(bg_color)
fig.subplots_adjust(
    hspace=0.2, left=0.05, right=0.95, wspace=0.05, bottom=0.06, top=0.85
)
axs = axs.flatten()


for i, (country, ax) in enumerate(zip(countries, axs)):
    df_sub = df.filter(col("Country") == country).drop_nulls()
    df_not_sub = df.filter(col("Country") != country)
    first = df_sub.select("Year", "Gini").head(1)
    last = df_sub.select("Year", "Gini").tail(1)

    sct_args = dict(color=colors[i], s=35, zorder=20)
    ax.scatter([first["Year"], last["Year"]], [first["Gini"], last["Gini"]], **sct_args)
    ax.plot(df_sub["Year"], df_sub["Gini"], zorder=10, color=colors[i], lw=2.5)

    ax.text(
        x=first["Year"][0] - relativedelta(months=15),
        y=first["Gini"][0],
        s=f"{first['Gini'][0]:.2f}",
        color=colors[i],
        font=font_bold,
        size=7,
        ha="right",
        va="center",
    )
    ax.text(
        x=last["Year"][0] + relativedelta(months=15),
        y=last["Gini"][0],
        s=f"{last['Gini'][0]:.2f}",
        color=colors[i],
        font=font_bold,
        size=7,
        va="center",
    )
    ax.axis("off")
    ax.set_facecolor(bg_color)
    ax.text(
        x=0.04,
        y=0.6,
        s=country,
        color=colors[i],
        transform=ax.transAxes,
        font=font_bold,
        size=11,
    )
    date_params = dict(
        color="grey",
        transform=ax.transAxes,
        font=font_italic,
        size=6,
        alpha=0.8,
    )
    ax.text(x=0.05, y=0, s=1980, **date_params)
    ax.text(x=0.95, y=0, s=2023, ha="right", **date_params)

    for sub_country in df_not_sub["Country"].unique().to_list():
        df_sub_country = df_not_sub.filter(col("Country") == sub_country)
        ax.plot(
            df_sub_country["Year"],
            df_sub_country["Gini"],
            color=colors[i],
            alpha=0.2,
            zorder=2,
        )

fig.text(
    x=0.5,
    y=0.97,
    s="Wealth inequality increases since the 80s",
    font=font_regular,
    size=20,
    ha="center",
    va="top",
    color="white",
)
fig.text(
    x=0.5,
    y=0.91,
    s="Gini index between 1980 and 2023 - The higher it is, the greater the inequality",
    font=font_italic,
    size=10,
    ha="center",
    va="top",
    color="grey",
)
fig.text(
    x=0.93,
    y=0.03,
    s="Data: World Inequality Database - Graphic: Joseph Barbier",
    font=font_regular,
    size=5,
    ha="right",
    va="top",
    color="grey",
)

plt.savefig("src/other/inequality/output.png", dpi=300, bbox_inches="tight")
