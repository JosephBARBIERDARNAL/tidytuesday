import pandas as pd
import matplotlib.pyplot as plt
from pyfonts import load_font
from drawarrow import ax_arrow

films = pd.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-03-11/pixar_films.csv"
)
public = pd.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-03-11/public_response.csv"
)

df = films.merge(public, on="film")
df["release_date"] = pd.to_datetime(df["release_date"])

repo_url = "https://github.com/googlefonts/roboto-2/blob/main/src/hinted"
lightfont = load_font(f"{repo_url}/Roboto-Light.ttf?raw=true")
italicfont = load_font(f"{repo_url}/Roboto-BlackItalic.ttf?raw=true")

bg_color = "#3f3f3f"
text_color = "#fff"

fig, ax = plt.subplots(figsize=(5, 9))
fig.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.scatter(
    x=df["rotten_tomatoes"],
    y=df["release_date"],
    alpha=0,
)

ax.set_xlim(30, 105)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.grid(axis="x", color="#676767", zorder=-1, lw=0.5)
ax.tick_params(labelsize=8, size=0, labelcolor=text_color)
ax.tick_params(axis="x", pad=5)
ax.tick_params(axis="y", pad=25)
ax.set_xticks(list(range(30, 91, 10)))

x0, x1 = ax.get_xlim()
y0, y1 = ax.get_ylim()

arrow_style = dict(
    ax=ax,
    color=text_color,
    clip_on=False,
    zorder=10,
    fill_head=False,
)
ax_arrow([x0 - 5.5, y0], [x1 + 5, y0], **arrow_style)
ax_arrow([x0 - 5, y0 - 30], [x0 - 5, y1], **arrow_style)

label_style = dict(color="#e1e1e1", transform=ax.transAxes, font=italicfont, size=8)
ax.text(x=-0.11, y=0.94, s="Year", rotation=90, **label_style)
ax.text(x=0.93, y=-0.02, s="Rating", **label_style)

for i, row in df.iterrows():
    ax.text(
        x=row["rotten_tomatoes"],
        y=row["release_date"],
        s=row["film"],
        ha="center",
        va="center",
        size=8,
        zorder=10,
        color="black",
        font=lightfont,
        bbox=dict(
            boxstyle="round",
            facecolor="#ceafaf",
            edgecolor=text_color,
            lw=0.5,
            pad=0.4,
        ),
    )

fig.text(
    x=0.07, y=0.91, s="Pixar films rating", color=text_color, font=lightfont, size=18
)
fig.text(
    x=0.07,
    y=0.89,
    s="Ratings (0 - 100) from Rotten Tomatoes",
    color=text_color,
    font=lightfont,
    size=9.7,
)
fig.text(
    x=0.9,
    y=0.895,
    s="TidyTuesday - 2025-03-11\nJoseph Barbier",
    font=lightfont,
    size=7,
    color=text_color,
    ha="right",
)

fig.savefig("src/2025/2025-03-11/output.png", dpi=300, bbox_inches="tight")
