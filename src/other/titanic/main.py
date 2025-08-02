import matplotlib.pyplot as plt
from plotjs import MagicPlot, css

from mpljourney import load_dataset

df = load_dataset("accident-london").sample(1500, random_state=0)
df["n_vehicles"] = (
    df["n_vehicles"]
    .astype(str)  # Convert to string explicitly
    .replace(
        {"1": "low", "2": "low", "3": "medium", "4": "medium", "5": "high", "6": "high"}
    )
)
df = df.sort_values("n_vehicles")
geo_df = load_dataset("london")

fig, ax = plt.subplots()
ax.axis("off")

geo_df.plot(color="#e5e5e5", ax=ax, ec="black", lw=0.3)
for group in df["n_vehicles"].unique():
    sub_df = df[df["n_vehicles"] == group]
    ax.scatter(
        sub_df["Longitude"],
        sub_df["Latitude"],
        s=50,
        ec="black",
        label=group,
    )
ax.legend()

(
    MagicPlot(fig)
    .add_tooltip(
        labels=df["n_vehicles"],
        groups=df["n_vehicles"],
    )
    .add_css(css.from_dict({".point.not-hovered": {"opacity": "0.05"}}))
    .save("src/other/titanic/index.html")
)
