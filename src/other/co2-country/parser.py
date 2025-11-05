import requests
from bs4 import BeautifulSoup
import pandas as pd


def parse_co2_emissions_table(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "datatable"})

    if not table:
        raise ValueError("Could not find the data table")

    data = []
    rows = table.find("tbody").find_all("tr")

    for row in rows:
        cells = row.find_all("td")

        if len(cells) < 7:
            continue

        rank = cells[0].get_text(strip=True)

        country_link = cells[1].find("a")
        country = (
            country_link.get_text(strip=True)
            if country_link
            else cells[1].get_text(strip=True)
        )
        co2_emissions = cells[2].get("data-order", cells[2].get_text(strip=True))
        year_change = cells[3].get("data-order", cells[3].get_text(strip=True))
        population = cells[4].get("data-order", cells[4].get_text(strip=True))
        per_capita = cells[5].get("data-order", cells[5].get_text(strip=True))
        share_of_world = cells[6].get("data-order", cells[6].get_text(strip=True))

        data.append(
            {
                "Rank": int(rank),
                "Country": country,
                "CO2_Emissions_tons_2022": int(co2_emissions),
                "Year_Change_percent": float(year_change) / 100,
                "Population_2022": int(population),
                "Per_Capita_tons": float(per_capita) / 100,
                "Share_of_World_percent": float(share_of_world) / 100,
            }
        )

    return pd.DataFrame(data)


url = "https://www.worldometers.info/co2-emissions/co2-emissions-by-country/"
df = parse_co2_emissions_table(url)
print(f"Successfully parsed {len(df)} countries\n")
df.to_csv("src/other/co2-country/co2_emissions_2022.csv", index=False)
