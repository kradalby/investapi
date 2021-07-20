from typing import Optional, Mapping, Any

import json

import requests
from bs4 import BeautifulSoup

from pydantic import BaseModel


class MorningstarFund(BaseModel):
    name: str
    isin: str
    price: float
    currency: str
    day_change: Optional[str] = None
    ongoing_charge: Optional[str] = None


def get_fund(isin: str) -> Optional[MorningstarFund]:
    uk = get_fund_uk(isin)
    if uk:
        return uk

    nor = get_fund_nor(isin)
    if nor:
        return nor


def get_morningstar_id(isin: str, country_code: str) -> Optional[str]:
    html_text = requests.get(
        f"https://www.morningstar.co.uk/{country_code}/util/SecuritySearch.ashx?q={isin.lower()}"
    ).text

    columns = html_text.split("|")

    if len(columns) < 2:
        return None

    json_string = columns[1]

    values = json.loads(json_string)

    if "i" in values:
        return values["i"]


def _parse_fund(html_text: str) -> Mapping[str, Any]:
    soup = BeautifulSoup(html_text, "html.parser")

    name = soup.find_all("div", {"class": "snapshotTitleBox"})[0].findChildren()[0].text

    overview = {}
    for row in soup.find_all("div", {"id": "overviewQuickstatsDiv"})[0].find_all("tr"):
        columns = row.find_all("td")

        for span in row.find_all("span"):
            span.decompose()

        if len(columns) > 2:
            key = columns[0].text.strip()
            value = columns[2].text.strip().replace("\xa0", " ")

            overview[key] = value

    overview["name"] = name
    return overview


def get_fund_nor(isin: str) -> Optional[MorningstarFund]:
    morningstar_id = get_morningstar_id(isin, "no")
    if not morningstar_id:
        print("No ms id found")
        return None

    html_text = requests.get(
        f"https://www.morningstar.no/no/funds/snapshot/snapshot.aspx?id={morningstar_id}"
    ).text

    overview = _parse_fund(html_text)

    fund = {}
    fund["name"] = overview["name"]

    if "ISIN" in overview:
        isin_value = overview["ISIN"]
        if isin_value.upper() != isin.upper():
            print("ISIN received is not same as requested")
            return None

        fund["isin"] = isin
    else:
        return None

    if "NAV" in overview:
        price_value = overview["NAV"]
        (currency, price_string) = price_value.split(" ")

        price = float(price_string.replace(",", "."))

        fund["currency"] = currency
        fund["price"] = price
    else:
        print("Price is not available")
        return None

    if "Endring 1 dag" in overview:
        change = overview["Endring 1 dag"]
        fund["previous_day_change"] = change

    if "Løpende kostnader" in overview:
        costs = overview["Løpende kostnader"]
        fund["running_costs"] = costs

    return MorningstarFund(**fund)


def get_fund_uk(isin: str) -> Optional[MorningstarFund]:
    morningstar_id = get_morningstar_id(isin, "uk")
    if not morningstar_id:
        print("No ms id found")
        return None

    html_text = requests.get(
        f"https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id={morningstar_id}"
    ).text

    overview = _parse_fund(html_text)

    fund = {}
    fund["name"] = overview["name"]

    if "ISIN" in overview:
        isin_value = overview["ISIN"]
        if isin_value.upper() != isin.upper():
            print("ISIN received is not same as requested")
            return None

        fund["isin"] = isin
    else:
        return None

    if "NAV" in overview:
        price_value = overview["NAV"]
        (currency, price_string) = price_value.split(" ")

        price = float(price_string.replace(",", "."))

        fund["currency"] = currency
        fund["price"] = price
    else:
        print("Price is not available")
        return None

    if "Day Change" in overview:
        change = overview["Day Change"]
        fund["day_change"] = change

    if "Ongoing Charge" in overview:
        costs = overview["Ongoing Charge"]
        fund["ongoing_charge"] = costs

    return MorningstarFund(**fund)
