import re
from datetime import date

import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection, Icons  # type: ignore[attr-defined]

TITLE = "Hýskov"
DESCRIPTION = (
    "Source for the municipal waste collection calendar of Hýskov, Czech Republic."
)
URL = "https://www.obechyskov.cz/obec/sluzby/odpady/"
COUNTRY = "cz"
SOURCE_CODEOWNERS = ["@bobek"]

TEST_CASES = {
    "Hýskov": {},
}

HOW_TO_GET_ARGUMENTS_DESCRIPTION = {
    "en": "No arguments are required. The source covers the whole village of Hýskov.",
    "de": "Es sind keine Argumente erforderlich. Die Quelle deckt die gesamte Gemeinde Hýskov ab.",
}

ICON_MAP = {
    "Plasty - kontejnery": Icons.PLASTIC_PACKAGING,
    "Sklo - kontejnery": Icons.GLASS,
    "Papír - kontejnery": Icons.PAPER,
    "Kov - kontejnery": Icons.METAL,
    "TKO - 1x týdně": Icons.GENERAL_WASTE,
    "Bio odpad": Icons.ORGANIC,
    "TKO - 1 x za 14 dní": Icons.GENERAL_WASTE,
    "TKO - 1x měsíčně": Icons.GENERAL_WASTE,
    "Nebezpečný odpad": Icons.HAZARDOUS,
    "Plast - žluté popelnice svoz od domu": Icons.PLASTIC_PACKAGING,
    "svoz pytlů po obci Hýskov": Icons.GENERAL_WASTE,
    "Papír - svoz modré popelnice od domu": Icons.PAPER,
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

# Number of months (starting with the current one) to fetch.
MONTHS_TO_FETCH = 13
# Stop early after this many consecutive empty months once data was found.
# The municipality publishes one calendar year at a time.
MAX_EMPTY_MONTHS = 2

TOOLTIP_ID_RE = re.compile(r"^tooltip(\d{4})(\d{2})(\d{2})$")


class Source:
    def __init__(self):
        pass

    def fetch(self) -> list[Collection]:
        session = requests.Session()
        session.headers.update(HEADERS)

        entries: list[Collection] = []
        today = date.today()
        year, month = today.year, today.month
        empty_streak = 0
        for _ in range(MONTHS_TO_FETCH):
            r = session.get(
                URL,
                params={"communal_month": month, "communal_year": year},
                timeout=30,
            )
            r.raise_for_status()
            month_entries = _parse_month(r.text, year, month)
            entries.extend(month_entries)

            if month_entries:
                empty_streak = 0
            else:
                empty_streak += 1
                if entries and empty_streak >= MAX_EMPTY_MONTHS:
                    break

            month += 1
            if month > 12:
                month = 1
                year += 1

        if not entries:
            raise ValueError(
                "No waste collection dates found on the Hýskov website for the "
                "current and next 12 months. The calendar may not be published "
                "yet or the website layout may have changed."
            )

        return entries


def _parse_month(month_html: str, year: int, month: int) -> list[Collection]:
    soup = BeautifulSoup(month_html, "html.parser")
    seen: set[tuple[date, str]] = set()
    entries: list[Collection] = []
    for tooltip in soup.select(
        'table.communal_services__table span.gcm-visually-hidden[id^="tooltip"]'
    ):
        match = TOOLTIP_ID_RE.match(str(tooltip.get("id", "")))
        if not match:
            continue
        y, m, d = (int(g) for g in match.groups())
        # The grid contains overflow days from the adjacent months; those are
        # picked up when the respective month is fetched.
        if y != year or m != month:
            continue
        collection_date = date(y, m, d)
        for b in tooltip.find_all("b"):
            waste_type = " ".join(b.get_text().split())
            if not waste_type or (collection_date, waste_type) in seen:
                continue
            seen.add((collection_date, waste_type))
            entries.append(
                Collection(collection_date, waste_type, icon=ICON_MAP.get(waste_type))
            )
    return entries
