import pandas as pd
import matplotlib.pyplot as plt
import dayplot as dp


df = pd.read_csv("src/other/calendar/pageview.csv")
df.columns = ["dates", "views"]
df.loc[len(df)] = ["2025-12-31", 0]
df.tail()

fig, axs = plt.subplots(figsize=(18, 5), nrows=3)

args = dict(
    vmax=df["views"].max(),
    vmin=df["views"].min(),
)
dp.calendar(
    dates=df["dates"],
    values=df["views"],
    start_date="2023-01-01",
    end_date="2024-01-01",
    ax=axs[0],
    **args,
)
dp.calendar(
    dates=df["dates"],
    values=df["views"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=axs[1],
    **args,
)
dp.calendar(
    dates=df["dates"],
    values=df["views"],
    start_date="2025-01-01",
    end_date="2025-12-31",
    ax=axs[2],
    **args,
)
text_args = dict(x=-4, y=3.5, size=20, rotation=90, color="#aaa", va="center")
axs[0].text(s="2023", **text_args)
axs[1].text(s="2024", **text_args)
axs[2].text(s="2025", **text_args)

plt.savefig("src/other/calendar/output.png", dpi=300, bbox_inches="tight")
