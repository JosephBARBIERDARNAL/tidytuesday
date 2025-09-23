import pandas as pd

url = "https://raw.githubusercontent.com/holtzy/the-python-graph-gallery/master/static/data/dataConsumerConfidence.csv"
df = pd.read_csv(url)

df = df.melt(id_vars=["Time"], var_name="country", value_name="value")
df["Time"] = pd.to_datetime(df["Time"], format="%b-%Y")
df = df.dropna()
df.head()
