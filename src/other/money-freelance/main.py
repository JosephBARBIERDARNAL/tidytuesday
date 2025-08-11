import matplotlib.pyplot as plt

months: list = [
    "October",
    "November",
    "December",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
]

values: list = [
    127,
    893,
    3188,
    2664,
    992,
    6140,
    7520,
    1939,
    2486,
    1358,
    4659,
]

fig, ax = plt.subplots(figsize=(11, 6))

ax.set_ylim(0, 7700)
ax.spines[["top", "left", "right"]].set_visible(False)
ax.tick_params(axis="x", pad=5, size=10)
ax.tick_params(axis="y", size=0)
ax.grid(axis="y", zorder=-2, alpha=0.3)
# ax.set_xticks()

ax.plot(months, values, color="black")
ax.scatter(months, values, s=80, color="black")

for i, value in enumerate(values):
    ax.text(
        x=i + 0.2,
        y=value + 200,
        s=f"{int(value)}€",
        bbox=dict(facecolor="white", alpha=0.9),
        zorder=100,
    )

ax.text(
    x=-0.5,
    y=8100,
    s="Monthly revenue of a freelance data scientist\n(after taxes, in Euro)",
    size=15,
    va="top",
)
ax.text(x=-0.3, y=-1000, s="2024", weight="bold", size=12)
ax.text(x=2.75, y=-1000, s="2025", weight="bold", size=12)
ax.text(
    x=10.4,
    y=-1100,
    s="barbierjoseph.com",
    style="italic",
    size=9,
    color="grey",
    ha="right",
)

fig.savefig("src/other/money-freelance/output.png", dpi=300, bbox_inches="tight")
