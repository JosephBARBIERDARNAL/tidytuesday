import matplotlib.pyplot as plt
import pandas as pd
from snaplot import Camera

plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300

df = pd.read_csv("src/other/world-population/population.csv")

# fmt: off
countries = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary",
    "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta",
    "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden"
]
df_eu = df[df["Country Name"].isin(countries)]


camera = Camera.start("movie")

fig, axs = plt.subplots(nrows=5, ncols=5, figsize=(10,10))
axs = axs.flatten()

for ax, country in zip(axs,countries):
    df_country = df_eu[df_eu["Country Name"]==country]
    ax.plot(df_country["Year"], df_country["Value"])

fig.savefig("cache.png")
camera.snap()

camera.stop("cache.gif", n_repeat_last_frame=10)
