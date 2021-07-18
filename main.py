from fastapi import FastAPI
from investpy import funds
from datetime import datetime, timedelta

app = FastAPI()

DATE_FORMAT = "%d/%m/%Y"


@app.get("/fund/{isin}")
async def get_fund(isin: str):
    return funds.search_funds("isin", isin).to_dict("records")[0]


@app.get("/fund/{isin}/name")
async def get_fund_name(isin: str):
    return funds.search_funds("isin", isin).to_dict("records")[0]["name"]


@app.get("/fund/{isin}/currency")
async def get_fund_currency(isin: str):
    return funds.search_funds("isin", isin).to_dict("records")[0]["currency"]


@app.get("/fund/{isin}/price")
async def get_fund_price(isin: str):
    fund = funds.search_funds("isin", isin).to_dict("records")[0]

    prices = funds.get_fund_historical_data(
        fund["name"],
        fund["country"],
        (datetime.now() - timedelta(days=7)).strftime(DATE_FORMAT),
        datetime.now().strftime(DATE_FORMAT),
    ).to_dict("index")

    last_date = sorted(prices.keys())[-1]

    last_price = prices[last_date]

    # if last_price["Currency"].upper() == "GBX":
    #     return last_price["Close"] * 1000
    return last_price["Close"]
