import polars as pl
import matplotlib.pyplot as plt
from pyfonts import load_google_font, set_default_font
import re

df = pl.read_csv("src/2026/2026-02-03/edible_plants.csv")

font_regular = load_google_font("Inter")
set_default_font(font_regular)
font_bold = load_google_font("Inter", weight="bold")


def parse_days(days_str):
    if not days_str or days_str == "NA":
        return None
    numbers = re.findall(r"\d+", str(days_str))
    if len(numbers) >= 2:
        return (int(numbers[0]) + int(numbers[1])) / 2
    elif len(numbers) == 1:
        return int(numbers[0])
    return None


df = df.with_columns(
    [
        pl.col("days_harvest")
        .map_elements(parse_days, return_dtype=pl.Float64)
        .alias("days_avg")
    ]
)

df_harvest = df.filter(pl.col("days_avg").is_not_null())

interesting_plants = [
    # The sprinters (< 50 days)
    "Cress",
    "Mizuna",
    "Radish",
    "Spinach (Perpetual)",
    "Beans (French)",
    # Middle distance (50-90 days)
    "Zucchini or Courgette",
    "Pea",
    "Tomatoes (Cherry)",
    "Carrots (Early)",
    "Onions (Perennial)",
    "Turnip",
    # Long haul (90-150 days)
    "Potatoes (Main crop)",
    "Leek",
    "Celery",
    "Artichoke (Globe)",
    "Winter Field Beans",
    # The marathon runner
    "Brussels Sprouts",
    "Ginger",
]

df_selected = df_harvest.filter(pl.col("common_name").is_in(interesting_plants))


def categorize_time(days):
    if days < 50:
        return "Quick crops"
    elif days < 90:
        return "Medium crops"
    else:
        return "Patient crops"


df_selected = df_selected.with_columns(
    [
        pl.col("days_avg")
        .map_elements(categorize_time, return_dtype=pl.String)
        .alias("time_category")
    ]
)

df_plot = df_selected.sort("days_avg")

fig, ax = plt.subplots(figsize=(14, 10), facecolor="#f8f9fa")
ax.set_facecolor("#f8f9fa")

y_positions = list(range(len(df_plot)))
for idx, row in enumerate(df_plot.iter_rows(named=True)):
    cultivation = row["cultivation"]
    days = row["days_avg"]
    name = row["common_name"]
    if idx == len(df_plot) - 1:
        color = "#6c757d"  # Dark grey for emphasis
        alpha = 0.9
    else:
        color = "#dee2e6"  # Light grey for all others
        alpha = 0.7

    ax.barh(
        idx,
        days,
        height=0.7,
        color=color,
        alpha=alpha,
        edgecolor="#f8f9fa",
        linewidth=1,
    )
    ax.text(-8, idx, name, ha="right", va="center", color="#2b2d42", size=13)
    ax.text(days + 3, idx, f"{int(days)}", va="center", color="#6c757d", size=14)

# Add section dividers and annotations for time categories
divider_y = []
prev_category = None
for idx, row in enumerate(df_plot.iter_rows(named=True)):
    category = row["time_category"]
    if prev_category and category != prev_category:
        divider_y.append(idx - 0.5)
    prev_category = category

# Draw subtle dividers
for y in divider_y:
    ax.axhline(
        y, color="#dee2e6", linewidth=1.5, linestyle="-", zorder=0, alpha=0.5, xmin=0.03
    )

category_positions = {"Quick crops": 1.5, "Medium crops": 6.5, "Patient crops": 11}
for category, y_pos in category_positions.items():
    ax.text(260, y_pos, category.upper(), va="center", color="#adb5bd", size=12)

ax.set_xlim(-9, 259)
ax.set_yticks([])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color("#dee2e6")
ax.spines["bottom"].set_linewidth(1.5)
ax.tick_params(axis="x", colors="#6c757d", labelsize=10, length=5)
ax.set_xlabel(
    "Days from planting to harvest",
    color="#495057",
    size=16,
    fontweight="bold",
    labelpad=15,
)

for x in [30, 60, 90, 120, 150, 180, 210, 240]:
    ax.axvline(x, color="#e9ecef", linewidth=0.8, linestyle="--", zorder=0, alpha=0.6)

ax.text(
    0.5,
    1.08,
    "How long until harvest?",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    color="#2b2d42",
    font=font_bold,
    size=40,
    fontweight="bold",
)
ax.text(
    0.5,
    1.03,
    "Days from planting to harvest for common edible plants",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    color="#6c757d",
    size=18,
)

ax.text(
    0.1,
    -0.11,
    "Data: The Edible Plant Database (GROW Observatory) | TidyTuesday 2026-02-03",
    transform=ax.transAxes,
    va="top",
    color="#adb5bd",
    size=11,
)

ax.text(
    0.1,
    -0.14,
    "Made by Joseph Barbier",
    transform=ax.transAxes,
    va="top",
    color="#495057",
    size=11,
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.1, top=0.92)
plt.savefig(
    "src/2026/2026-02-03/output.png",
    dpi=150,
    facecolor="#f8f9fa",
    bbox_inches="tight",
    pad_inches=0.4,
)
