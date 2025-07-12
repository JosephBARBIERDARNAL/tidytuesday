import pandas as pd
import matplotlib.pyplot as plt
from pyfonts import load_google_font
from highlight_text import ax_text


df = pd.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/refs/heads/main/data/2025/2025-07-01/weekly_gas_prices.csv"
)
df = df[df["grade"] == "all"]
df["date"] = pd.to_datetime(df["date"])
gas = (
    df[(df["fuel"] == "gasoline") & (df["formulation"] == "all")]
    .sort_values("date")
    .reset_index(drop=True)
)
gas_subprime = gas[(gas["date"] >= "2007-01-01") & (gas["date"] <= "2010-12-31")]
gas_war = gas[gas["date"] >= "2020-01-01"]

font = load_google_font("Inter")
boldfont = load_google_font("Inter", weight="bold")
color = "#0077b6"
bg_color = "#f2e8cf"

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
plt.subplots_adjust(top=0.8, bottom=0.15)
fig.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
ax.axis("off")
ax.set_ylim(1, gas["price"].max() * 1.05)

first_y = gas["price"].values[0]
first_x = gas["date"].values[0]
last_y = gas["price"].values[-1]
last_x = gas["date"].values[-1]
max_x = gas.loc[gas["price"].idxmax(), "date"]
max_y = gas["price"].max()
max_x_suprime = gas_subprime.loc[gas_subprime["price"].idxmax(), "date"]
min_x_suprime = gas_subprime.loc[gas_subprime["price"].idxmin(), "date"]
max_y_suprime = gas_subprime["price"].max()
min_y_suprime = gas_subprime["price"].min()
min_x_war = gas_war.loc[gas_war["price"].idxmin(), "date"]
min_y_war = gas_war["price"].min()

ax.plot(gas["date"], gas["price"], lw=1.5, clip_on=False, color=color)
scatter_args = dict(s=100, clip_on=False, color=color)
ax.scatter(
    [first_x, last_x, max_x, max_x_suprime, min_x_suprime, min_x_war],
    [first_y, last_y, max_y, max_y_suprime, min_y_suprime, min_y_war],
    **scatter_args,
)
f_and_l_args = dict(
    va="center",
    font=boldfont,
    clip_on=False,
    fontsize=12,
)
ax.text(
    0.98,
    last_y,
    f"${last_y:,.1f}",
    ha="left",
    transform=ax.get_yaxis_transform(),
    **f_and_l_args,
)
ax.text(
    0.02,
    first_y,
    f"${first_y:,.2f}",
    ha="right",
    transform=ax.get_yaxis_transform(),
    **f_and_l_args,
)
ax.text(
    max_x + pd.Timedelta(45, "w"), max_y, f"${max_y:,.1f}", ha="left", **f_and_l_args
)
ax.text(
    max_x_suprime - pd.Timedelta(45, "w"),
    max_y_suprime,
    f"${max_y_suprime:,.1f}",
    ha="right",
    **f_and_l_args,
)
ax.text(
    min_x_suprime + pd.Timedelta(45, "w"),
    min_y_suprime,
    f"${min_y_suprime:,.1f}",
    ha="left",
    **f_and_l_args,
)
ax.text(
    min_x_war - pd.Timedelta(45, "w"),
    min_y_war,
    f"${min_y_war:,.1f}",
    ha="right",
    **f_and_l_args,
)

year_args = dict(ha="center", va="top", size=20, font=font, alpha=0.3)
ax.text(pd.to_datetime(str(first_x)[:10]), 0.5, "1993", **year_args)
ax.text(pd.to_datetime(str(last_x)[:10]), 0.5, "2025", **year_args)

title_args = dict(ha="left", va="top", transform=ax.transAxes, clip_on=False)
y = 1.18
ax.text(
    x=-0.05,
    y=y,
    s="30 years of US gas prices",
    size=35,
    font=boldfont,
    **title_args,
)
ax_text(
    x=pd.to_datetime("1990-01-01"),
    y=5.4,
    s="<Data>: U.S. Energy Information Administration\n<Graphic>: Joseph Barbier",
    highlight_textprops=[{"font": boldfont}, {"font": boldfont}],
    color="#6B6B6B",
    size=8,
    font=font,
    ax=ax,
    **title_args,
)

ax.axvspan(
    pd.to_datetime("2007-12-01"),
    pd.to_datetime("2009-09-01"),
    ymin=0.1,
    ymax=0.78,
    color="grey",
    alpha=0.1,
    zorder=10,
    clip_on=False,
)
ax.text(
    x=pd.to_datetime("2008-10-01"),
    y=4.6,
    s="Subprime",
    font=font,
    color="grey",
    ha="center",
    alpha=0.6,
)

ax.axvspan(
    pd.to_datetime("2019-10-01"),
    pd.to_datetime("2023-02-01"),
    ymin=0.1,
    ymax=0.98,
    color="grey",
    alpha=0.1,
    zorder=10,
    clip_on=False,
)
ax.text(
    x=pd.to_datetime("2021-06-01"),
    y=1.25,
    s="Inflation\nRussia-Ukraine war\nOPEC+ cuts",
    font=font,
    color="grey",
    ha="center",
    va="top",
    alpha=0.6,
)

fig.savefig("src/2025/2025-07-01/output.png", dpi=300)
