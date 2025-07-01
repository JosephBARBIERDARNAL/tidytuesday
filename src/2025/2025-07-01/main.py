import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pyfonts import load_google_font
from datetime import timedelta


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

ax.plot(gas["date"], gas["price"], lw=1.5, clip_on=False, color=color)
scatter_args = dict(s=100, clip_on=False, color=color)
ax.scatter(
    [first_x, last_x, max_x, max_x_suprime, min_x_suprime],
    [first_y, last_y, max_y, max_y_suprime, min_y_suprime],
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

year_args = dict(ha="center", va="top", size=20, font=font, alpha=0.3)
ax.text(pd.to_datetime(str(first_x)[:10]), 0.5, "1993", **year_args)
ax.text(pd.to_datetime(str(last_x)[:10]), 0.5, "2025", **year_args)

title_args = dict(ha="center", va="top", transform=ax.transAxes, clip_on=False)
y = 1.2
ax.text(
    x=0.5,
    y=y,
    s="30 years of US gas prices",
    size=35,
    font=boldfont,
    **title_args,
)
ax.text(
    x=0.5,
    y=y - 0.14,
    s="Since the 90's, gas price in US has been something interesting",
    color="#6B6B6B",
    size=20,
    font=font,
    **title_args,
)

fig.savefig("src/2025/2025-07-01/output.png", dpi=300)
