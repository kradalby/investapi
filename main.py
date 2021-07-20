from typing import Mapping, Any, Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

from expiringdict import ExpiringDict

from investpy import funds
import yfinance as yf

from pandas import Timestamp


DATE_FORMAT = "%d/%m/%Y"

app = FastAPI()
Instrumentator().instrument(app).expose(app)

STOCKS = ExpiringDict(max_len=100, max_age_seconds=300)
FUNDS = ExpiringDict(max_len=100, max_age_seconds=3600)


async def fetch_stock(ticker: str) -> Optional[yf.Ticker]:
    if ticker in STOCKS.keys():
        return STOCKS[ticker]

    tick = yf.Ticker(ticker)

    # Tickers that has left than 2 items in their info seems to be non existent or delisted
    if len(tick.info.keys()) < 5:
        return None

    STOCKS[ticker] = tick

    return tick


async def fetch_fund(isin: str) -> Optional[Mapping[str, Any]]:
    if isin in FUNDS.keys():
        return FUNDS[isin]

    try:
        fund = funds.search_funds("isin", isin).to_dict("records")[0]
        FUNDS[isin] = fund

        return fund
    except RuntimeError:
        return None


@app.get("/v1/fund/{isin}")
async def get_fund(isin: str):
    fund = await fetch_fund(isin)
    if not fund:
        raise HTTPException(status_code=404, detail="not found")

    return fund


@app.get("/v1/fund/{isin}/name")
async def get_fund_name(isin: str):
    fund = await fetch_fund(isin)
    if not fund:
        raise HTTPException(status_code=404, detail="not found")

    name: str = fund["name"]
    return name


@app.get("/v1/fund/{isin}/currency")
async def get_fund_currency(isin: str):
    fund = await fetch_fund(isin)
    if not fund:
        raise HTTPException(status_code=404, detail="not found")

    currency: str = fund["currency"]
    if currency.upper() == "GBX":
        return "GBP".encode("utf-8")
    return currency.encode("utf-8")


@app.get("/v1/fund/{isin}/price")
async def get_fund_price(isin: str):
    fund = await fetch_fund(isin)
    if not fund:
        raise HTTPException(status_code=404, detail="not found")

    prices: Mapping[Timestamp, Mapping] = funds.get_fund_historical_data(
        fund["name"],
        fund["country"],
        (datetime.now() - timedelta(days=7)).strftime(DATE_FORMAT),
        datetime.now().strftime(DATE_FORMAT),
    ).to_dict("index")

    last_date = sorted(prices.keys())[-1]

    last_price = prices[last_date]

    close_price: int = last_price["Close"]

    if last_price["Currency"].upper() == "GBX":
        return close_price / 100
    return close_price


@app.get("/v1/stock/{ticker}")
async def get_stock(ticker: str):
    tick = await fetch_stock(ticker)
    if not tick:
        raise HTTPException(status_code=404, detail="not found")

    info: Mapping[str, Any] = tick.info
    return info


@app.get("/v1/stock/{ticker}/name")
async def get_stock_name(ticker: str):
    tick = await fetch_stock(ticker)
    if not tick:
        raise HTTPException(status_code=404, detail="not found")

    info: Mapping[str, Any] = tick.info
    if "shortName" in info.keys():
        name: str = info["shortName"]
        return name

    name: str = info["longName"]
    return name


@app.get("/v1/stock/{ticker}/currency")
async def get_stock_currency(ticker: str):
    tick = await fetch_stock(ticker)
    if not tick:
        raise HTTPException(status_code=404, detail="not found")

    info: Mapping[str, Any] = tick.info
    currency: str = info["currency"]

    if currency.upper() == "GBX" or currency == "GBp":
        return "GBP".encode("utf-8")
    return currency.encode("utf-8")


@app.get("/v1/stock/{ticker}/price")
async def get_stock_price(ticker: str):
    tick = await fetch_stock(ticker)
    if not tick:
        raise HTTPException(status_code=404, detail="not found")

    info: Mapping[str, Any] = tick.info
    price: float = info["regularMarketPrice"]
    currency: str = info["currency"]

    if currency.upper() == "GBX" or currency == "GBp":
        return price / 100
    return price
