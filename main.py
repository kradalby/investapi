from typing import Mapping, Any, Optional

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

from expiringdict import ExpiringDict

import yfinance as yf
import morningstar


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


async def fetch_fund(isin: str) -> Optional[morningstar.MorningstarFund]:
    if isin in FUNDS.keys():
        return FUNDS[isin]

    fund = morningstar.get_fund(isin)
    if fund:
        FUNDS[isin] = fund

        return fund


@app.get("/v1/fund/{isin}")
async def get_fund(isin: str) -> morningstar.MorningstarFund:
    fund = await fetch_fund(isin)
    if not fund:
        raise HTTPException(status_code=404, detail="not found")

    return fund


@app.get("/v1/fund/{isin}/name")
async def get_fund_name(isin: str) -> str:
    fund = await fetch_fund(isin)
    if not fund:
        raise HTTPException(status_code=404, detail="not found")

    return fund.name


@app.get("/v1/fund/{isin}/currency")
async def get_fund_currency(isin: str) -> str:
    fund = await fetch_fund(isin)
    if not fund:
        raise HTTPException(status_code=404, detail="not found")

    if fund.currency.upper() == "GBX":
        return "GBP"
    return fund.currency


@app.get("/v1/fund/{isin}/price")
async def get_fund_price(isin: str) -> float:
    fund = await fetch_fund(isin)
    if not fund:
        raise HTTPException(status_code=404, detail="not found")

    if fund.currency.upper() == "GBX":
        return fund.price / 100
    return fund.price


@app.get("/v1/stock/{ticker}")
async def get_stock(ticker: str) -> Mapping[str, Any]:
    tick = await fetch_stock(ticker)
    if not tick:
        raise HTTPException(status_code=404, detail="not found")

    info: Mapping[str, Any] = tick.info
    return info


@app.get("/v1/stock/{ticker}/name")
async def get_stock_name(ticker: str) -> str:
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
async def get_stock_currency(ticker: str) -> str:
    tick = await fetch_stock(ticker)
    if not tick:
        raise HTTPException(status_code=404, detail="not found")

    info: Mapping[str, Any] = tick.info
    currency: str = info["currency"]

    if currency.upper() == "GBX" or currency == "GBp":
        return "GBP"
    return currency


@app.get("/v1/stock/{ticker}/price")
async def get_stock_price(ticker: str) -> float:
    tick = await fetch_stock(ticker)
    if not tick:
        raise HTTPException(status_code=404, detail="not found")

    info: Mapping[str, Any] = tick.info
    price: float = info["regularMarketPrice"]
    currency: str = info["currency"]

    if currency.upper() == "GBX" or currency == "GBp":
        return price / 100
    return price
