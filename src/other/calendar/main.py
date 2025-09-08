import matplotlib.pyplot as plt
import dayplot as dp
import pandas as pd
from pyfonts import load_google_font
from pypalettes import load_cmap


df = pd.read_csv("src/other/calendar/pageview.csv")
df.columns = ["dates", "views"]
df.head()

cmap = load_cmap("Mushroom", cmap_type="continuous", reverse=True)

fig, ax = plt.subplots(figsize=(15, 5))

dp.calendar(
    dates=df["dates"],
    values=df["views"],
    legend=True,
    legend_bins=8,
    ax=ax,
    cmap=cmap,
)

thing = "capybara"
fig.text(
    x=0.5,
    y=0.87,
    s=f"Is {thing} not a thing anymore?!",
    size=25,
    ha="center",
    font=load_google_font("Roboto", weight="bold"),
)
fig.text(
    x=0.5,
    y=0.8,
    s=f"Daily visits of the '{thing.title()}' Wikipedia page in 2025",
    size=13,
    ha="center",
    color="grey",
    font=load_google_font("Roboto", italic=True),
)
fig.text(
    x=0.87,
    y=0.2,
    s="Made with dayplot, by Joseph Barbier",
    size=8,
    ha="right",
    color="darkgrey",
    font=load_google_font("Roboto"),
)

plt.savefig("src/other/calendar/output.png", dpi=300, bbox_inches="tight")
