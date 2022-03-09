from datetime import datetime, timedelta
from textwrap import dedent
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import pandas as pd
import seaborn as sns


# Best estimate of the total energy generation capacity at the end of 2021.
# Updated 2022-03-09.
before_2022_kw = {
    "biomasse-brutto": 8744302,
    "solar-brutto": 60081486,
    "verbrennung-brutto": 90466235,
    "wasser-brutto": 5665961,
    "wind-land-brutto": 55928909,
    "wind-see-brutto": 7786818,
}

# Source: https://www.wiwo.de/politik/deutschland/tracking-der-energiewende-1-von-allem-zu-wenig/27981020.html
# Archive: https://archive.is/i6XTk
increase_gw_per_year = {
    "solar-brutto": {
        2022: 7,
        2023: 9,
        2024: 13,
        2025: 16,
        2026: 18,
        2027: 19,
        2028: 20,
        2029: 20,
        2030: 20,
    },
    "wind-land-brutto": {
        2022: 3,
        2023: 5,
        2024: 6,
        2025: 7,
        2026: 9,
        2027: 10,
        2028: 10,
        2029: 10,
        2030: 9,
    },
    "wind-see-brutto": {
        2022: 0.5,
        2023: 0.5,
        2024: 0.5,
        2025: 2,
        2026: 1,
        2027: 1,
        2028: 4,
        2029: 6,
        2030: 7,
    },
}

name = {
    "biomasse-brutto": "Biomasse",
    "solar-brutto": "Solar",
    "verbrennung-brutto": "Verbrennung",
    "wasser-brutto": "Wasser",
    "wind-land-brutto": "Wind an Land",
    "wind-see-brutto": "Wind auf See",
}


def expected_kw(typ, date):
    # date = datetime.strptime(date, "%Y-%m-%d")
    if date.year < 2022 or date.year > 2030:
        raise "calculation only valid for 2022 to 2030"

    expected_kw_kw = before_2022_kw[typ]
    if expected_kw_kw is None:
        raise f"no base value known for {typ}"

    for year, gw in increase_gw_per_year[typ].items():
        if year < date.year:
            expected_kw_kw += gw * 1e6

    gw_per_year = increase_gw_per_year[typ][date.year]
    if gw_per_year is None:
        raise f"no increase known for {typ}, {date.year}"

    days_in_year = (datetime(date.year + 1, 1, 1) - datetime(date.year, 1, 1)).days
    days_since_jan1 = (date - datetime(date.year, 1, 1)).days
    expected_kw_kw += gw_per_year * 1e6 * days_since_jan1 / days_in_year
    return expected_kw_kw


def actual(typ, date):
    df = pd.read_json("stat.json", lines=True)
    return df[(df["query"] == typ) & (df["date"] == date)]["result"].values[0]


def main():
    typ = "solar-brutto"

    d2 = datetime.today()
    d2 = datetime(year=d2.year, month=d2.month, day=d2.day)
    d1 = d2 - timedelta(days=7)

    typs = ["solar-brutto", "wind-land-brutto", "wind-see-brutto"]

    records = []
    for typ in typs:
        records.extend(
            [
                {
                    "kind": "ist",
                    "typ": typ,
                    "date": d1,
                    "value": actual(typ, d1),
                },
                {
                    "kind": "ist",
                    "typ": typ,
                    "date": d2,
                    "value": actual(typ, d2),
                },
                {
                    "kind": "soll",
                    "typ": typ,
                    "date": d1,
                    "value": expected_kw(typ, d1),
                },
                {
                    "kind": "soll",
                    "typ": typ,
                    "date": d2,
                    "value": expected_kw(typ, d2),
                },
            ]
        )

    sns.set_theme()
    sns.set_style("white")
    sns.set_palette("colorblind")
    sns.set_context("talk")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    df = pd.DataFrame.from_records(records)
    df["value"] = df["value"] * 1000  # kW to W

    for i, typ in enumerate(typs):
        data = df[df["typ"] == typ]
        ax = sns.lineplot(
            data=data,
            x="date",
            y="value",
            hue="kind",
            marker="o",
            dashes=False,
            lw=5,
            markersize=15,
            ax=axes[i],
        )

        ax.set_title(name[typ])

        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_major_formatter(ticker.EngFormatter(unit="W", places=2))
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.yaxis.grid(which="major", linewidth=1)

        date_locator = dates.DayLocator(bymonthday=[d1.day, d2.day])
        ax.xaxis.set_major_locator(date_locator)
        ax.xaxis.set_major_formatter(dates.AutoDateFormatter(date_locator))

    for ax in axes:
        # https://www.statology.org/matplotlib-legend-order/
        handles, labels = ax.get_legend_handles_labels()
        order = [1, 0]
        ax.legend(
            [handles[idx] for idx in order], [labels[idx].title() for idx in order]
        )
        ax.set_xlabel(None)
        ax.set_ylabel(None)

    axes[0].set_xlabel(None)
    axes[0].set_ylabel("Bruttoleistung\n")

    plt.tight_layout()
    plt.savefig("plot.png", pad_inches=0.3)

    print(
        f"Zuwachs erneuerbarer Energien von {d1.strftime('%Y-%m-%d')} bis {d2.strftime('%Y-%m-%d')}:"
    )
    for typ in typs:
        data = df[df["typ"] == typ]

        d1_actual = data[data["date"] == d1.strftime("%Y-%m-%d")]["value"].values[0]
        d2_actual = data[data["date"] == d2.strftime("%Y-%m-%d")]["value"].values[0]
        diff_actual = d2_actual - d1_actual

        d1_actual = f"{(d1_actual * 1e-9):.02f} GW"
        d2_actual = f"{(d2_actual * 1e-9):.02f} GW"
        diff_actual = f"{(diff_actual * 1e-9):+.02f} GW"

        d1_planned = f"{(expected_kw(typ, d1) * 1e-6):.02f} GW"
        d2_planned = f"{(expected_kw(typ, d2) * 1e-6):.02f} GW"
        diff_planned = (
            f"{((expected_kw(typ, d2) - expected_kw(typ, d1)) * 1e-6):+.02f} GW"
        )

        print(
            f"• {name[typ]}: {d2_actual} ({diff_actual}) registriert, Sollwert {d2_planned}."
        )

    print(
        """
Definitionen und Quellen: https://marktstammdatenregister.dev/bot"""
    )


if __name__ == "__main__":
    main()
