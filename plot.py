from datetime import datetime
from textwrap import dedent
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns


def soll(date):
    start_date = datetime.strptime("2022-01-01", "%Y-%m-%d")
    start_value_kw = 63683577.581
    per_day_kw = 7000000.0 / 365

    days = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    return start_value_kw + per_day_kw * days


df = pd.read_json("stat.json", lines=True)
df = df[df["query"] == "wind-brutto"]

d1 = "2022-03-02"
d2 = "2022-03-06"

old = df[df["date"] == d1]["result"].values[0]
new = df[df["date"] == d2]["result"].values[0]

df = pd.DataFrame.from_records(
    [
        {"kind": "ist", "date": d1, "value": old},
        {"kind": "ist", "date": d2, "value": new},
        {"kind": "soll", "date": d1, "value": soll(d1)},
        {"kind": "soll", "date": d2, "value": soll(d2)},
    ]
)
df["value"] = df["value"] * 1000

sns.set_context("talk", font_scale=1.5)
ax = sns.lineplot(
    data=df,
    x="date",
    y="value",
    hue="kind",
    marker="o",
    dashes=False,
    lw=5,
    markersize=15,
)
plt.xlabel("Datum")
plt.ylabel("Bruttoleistung\n")

# https://www.statology.org/matplotlib-legend-order/
handles, labels = plt.gca().get_legend_handles_labels()
order = [1, 0]
plt.legend([handles[idx] for idx in order], [labels[idx].title() for idx in order])

ax.yaxis.set_major_locator(ticker.AutoLocator())
ax.yaxis.set_major_formatter(ticker.EngFormatter(unit="W", places=2))
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.grid(which="major", linewidth=1)

plt.savefig("stat.png", bbox_inches="tight", pad_inches=0.3)

print(
    dedent(
        f"""
        Das Defizit im Ausbau der Solarenergie stieg zwischen {d1} und {d2} von {((soll(d1) - old) * 1e-3):.0f} MW auf {((soll(d2) - new) * 1e-3):.0f} MW.
        """
    )
)
