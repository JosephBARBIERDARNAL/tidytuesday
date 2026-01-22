import polars as pl
import matplotlib.pyplot as plt
from pyfonts import load_font

# =============================================================================
# DESIGN PHILOSOPHY
# =============================================================================
# Story: A small community of dedicated astrophotographers has collectively
# contributed hundreds of images to NASA's APOD over 18 years. Each has their
# specialty - deep sky hunters chase galaxies and nebulae, while night sky
# photographers capture auroras and the Milky Way from Earth.
#
# Design principles:
# - High data-to-ink ratio: no gridlines, minimal decorations
# - Direct labeling instead of legends
# - Space-themed dark background (appropriate for astronomy)
# - Horizontal bars for easy name reading
# - Color encodes subject specialty, not just decoration
# =============================================================================

# Load data
df = pl.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-20/apod.csv"
)

# Load fonts
font_regular = load_font(
    "https://github.com/google/fonts/raw/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf"
)
font_bold = load_font(
    "https://github.com/google/fonts/raw/main/ofl/spacemono/SpaceMono-Bold.ttf"
)


# Classify subjects based on title
def classify_subject(title):
    title_lower = title.lower()
    if any(x in title_lower for x in ["nebula", "nebulae"]):
        return "Nebulae"
    elif any(
        x in title_lower
        for x in ["galaxy", "galaxies", "andromeda", "m31", "m33", "m51", "m81", "m82"]
    ):
        return "Galaxies"
    elif any(x in title_lower for x in ["milky way"]):
        return "Milky Way"
    elif any(x in title_lower for x in ["aurora", "northern light", "southern light"]):
        return "Auroras"
    elif any(x in title_lower for x in ["moon", "lunar"]):
        return "Moon"
    elif any(x in title_lower for x in ["eclipse"]):
        return "Eclipses"
    elif any(x in title_lower for x in ["comet"]):
        return "Comets"
    elif any(x in title_lower for x in ["sun", "solar", "sunspot"]):
        return "Sun"
    elif any(
        x in title_lower for x in ["mars", "jupiter", "saturn", "venus", "planet"]
    ):
        return "Planets"
    else:
        return "Other"


# Get top 10 photographers
top_photogs = (
    df.filter(~pl.col("copyright").is_in(["NA", ""]))
    .group_by("copyright")
    .agg(pl.len().alias("count"))
    .sort("count", descending=True)
    .head(10)
)

# Build data for stacked bars
photographers = []
subject_data = {
    "Galaxies": [],
    "Nebulae": [],
    "Milky Way": [],
    "Moon": [],
    "Planets": [],
    "Auroras": [],
    "Comets": [],
    "Sun": [],
    "Eclipses": [],
    "Other": [],
}

for row in top_photogs.iter_rows():
    name, count = row
    photographers.append(name)
    photos = df.filter(pl.col("copyright") == name)

    subject_counts = {}
    for title in photos["title"].to_list():
        subj = classify_subject(title)
        subject_counts[subj] = subject_counts.get(subj, 0) + 1

    for subj in subject_data.keys():
        subject_data[subj].append(subject_counts.get(subj, 0))

# Reverse for bottom-to-top plotting (highest at top)
photographers = photographers[::-1]
for subj in subject_data:
    subject_data[subj] = subject_data[subj][::-1]

# Colors - vibrant cosmic palette with better contrast
colors = {
    "Galaxies": "#5B9BD5",  # Bright blue (spiral arms)
    "Nebulae": "#FF6B35",  # Vibrant orange-red (emission nebulae)
    "Milky Way": "#F4E04D",  # Bright yellow (galactic core)
    "Moon": "#E8E8E8",  # Bright silver
    "Planets": "#70D6FF",  # Light cyan (gas giants)
    "Auroras": "#06FFA5",  # Bright emerald (northern lights)
    "Comets": "#C77DFF",  # Bright purple (ion tails)
    "Sun": "#FFB703",  # Bright amber (solar corona)
    "Eclipses": "#8B8B8B",  # Medium gray
    "Other": "#4A4A4A",  # Darker gray (unclassified)
}

# Create figure
fig, ax = plt.subplots(figsize=(12, 8), facecolor="#0B1E38")
ax.set_facecolor("#0B1E38")

# Plot stacked horizontal bars
y_pos = range(len(photographers))
left = [0] * len(photographers)

# Order subjects by total contribution for better visual hierarchy
subject_order = [
    "Galaxies",
    "Nebulae",
    "Milky Way",
    "Moon",
    "Planets",
    "Auroras",
    "Comets",
    "Sun",
    "Eclipses",
    "Other",
]

for subj in subject_order:
    values = subject_data[subj]
    bars = ax.barh(
        y_pos,
        values,
        left=left,
        color=colors[subj],
        label=subj if sum(values) > 0 else None,
        height=0.7,
        edgecolor="#0B1E38",
        linewidth=0.5,
    )
    left = [l + v for l, v in zip(left, values)]

# Add photographer names and annotations
for i, (name, total) in enumerate(zip(photographers, left)):
    # Name on the left (outside plot area)
    ax.text(
        -2,
        i,
        name,
        ha="right",
        va="center",
        color="#E8E8E8",
        fontproperties=font_regular,
        fontsize=12,
    )
    # Total count at the end of bar
    ax.text(
        total + 1.5,
        i,
        str(total),
        ha="left",
        va="center",
        color="#888888",
        fontproperties=font_regular,
        fontsize=10,
    )

# Add direct annotations on bars for main subjects (where segments are large enough)
cumulative_left = [0] * len(photographers)
for subj in subject_order:
    values = subject_data[subj]
    for i, value in enumerate(values):
        if value >= 5:  # Only label segments with 5+ images
            bar_center = cumulative_left[i] + value / 2
            # Determine text color for contrast
            text_color = "#FFFFFF" if subj in ["Nebulae", "Comets"] else "#000000"
            text_color = (
                "#CCCCCC" if subj == "Other" else text_color
            )  # Lighter gray for "Other"
            ax.text(
                bar_center,
                i,
                subj.replace(" ", "\n") if " " in subj else subj,
                ha="center",
                va="center",
                color=text_color,
                fontproperties=font_regular,
                fontsize=9.5,
                fontweight="bold",
            )
        cumulative_left[i] += value

# Add strategic annotations for specific unlabeled small segments
# Annotate a few key examples to identify colors without labels

# Comets annotation (purple) - on Martin Pugh's or Adam Block's bar
martin_idx = photographers.index("Martin Pugh")
offset = sum(
    [
        subject_data[s][martin_idx]
        for s in subject_order[: subject_order.index("Comets")]
    ]
)
comet_center = offset + subject_data["Comets"][martin_idx] / 2
ax.annotate(
    "Comets",
    xy=(comet_center, martin_idx),
    xytext=(comet_center + 2, martin_idx + 0.5),
    ha="left",
    color="#C77DFF",
    fontproperties=font_regular,
    fontsize=7.5,
    arrowprops=dict(arrowstyle="-", color="#C77DFF", lw=0.8),
)

# Sun annotation (orange/amber) - on Babak Tafreshi's bar
babak_idx = photographers.index("Babak Tafreshi")
offset = sum(
    [subject_data[s][babak_idx] for s in subject_order[: subject_order.index("Sun")]]
)
sun_center = offset + subject_data["Sun"][babak_idx] / 2
ax.annotate(
    "Sun",
    xy=(sun_center, babak_idx),
    xytext=(sun_center, babak_idx),
    ha="center",
    va="center",
    color="black",
    fontproperties=font_regular,
    fontsize=7.5,
)

# Eclipse annotation (medium gray) - on Tunç Tezel's bar
tunc_idx = photographers.index("Tunç Tezel")
offset = sum(
    [
        subject_data[s][tunc_idx]
        for s in subject_order[: subject_order.index("Eclipses")]
    ]
)
eclipse_center = offset + subject_data["Eclipses"][tunc_idx] / 2
ax.annotate(
    "Eclipse",
    xy=(eclipse_center, tunc_idx - 0.15),
    xytext=(eclipse_center + 5, tunc_idx - 0.55),
    ha="center",
    color="#8B8B8B",
    fontproperties=font_regular,
    fontsize=7.5,
    arrowprops=dict(arrowstyle="-", color="white", lw=0.8),
)

# Clean up axes - maximize data-to-ink ratio
ax.set_yticks([])
ax.set_xlim(-8, 70)  # Start closer to 0 with space for names
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color("#333333")
ax.tick_params(axis="x", colors="#666666", labelsize=9)
ax.set_xlabel(
    "Total number of photographs featured in APOD",
    color="#888888",
    fontproperties=font_regular,
    fontsize=10,
    fontweight="bold",
)

# Add subtle note about "Other" category
ax.text(
    0.5,
    -0.08,
    '"Other" includes subjects not classified into main categories (e.g., unique phenomena, Earth features, spacecraft)',
    transform=ax.transAxes,
    ha="center",
    va="top",
    color="#666666",
    fontproperties=font_regular,
    fontsize=9,
    style="italic",
)

# Add subtle note about "Other" category
ax.text(
    1,
    -0.08,
    "Made by Joseph Barbier",
    transform=ax.transAxes,
    ha="right",
    va="top",
    color="#fefae0",
    fontproperties=font_regular,
    fontsize=9,
    style="italic",
)

# Title
ax.text(
    0.5,
    1.1,
    "The Guardians of the Night Sky",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    color="#E8E8E8",
    fontproperties=font_bold,
    fontsize=27,
)
ax.text(
    0.5,
    1.03,
    "Top 10 astrophotographers by total number of images featured in NASA's APOD (2007-2025)",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    color="#888888",
    fontproperties=font_regular,
    fontsize=15,
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.12, top=0.88)
plt.savefig(
    "src/2026/2026-01-20/output.png",
    dpi=150,
    facecolor="#0B1E38",
    bbox_inches="tight",
    pad_inches=0.3,
)
plt.close()
