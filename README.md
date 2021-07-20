# InvestAPI

Small web service to get name, price and currency for Google Sheets.

Funds are scraped from [Morningstar](https://www.morningstar.co.uk/uk/)(Currently Norway and United Kingdom is supported)
and Stocks are fetched from Yahoo Finance with [yfinance](https://github.com/ranaroussi/yfinance).

## Install

Build and run docker image, it will serve on port 8000

or

Install dependencies with [Poetry](https://python-poetry.org):

```bash
poetry install
```

And run [uvicorn](https://www.uvicorn.org):

```bash
poetry run uvicorn main:app --reload
```

## Usage

See all the endpoints in the OpenAPI overview (http://localhost:8000/docs)

Provides convenient endpoints only returning the desired values:

```bash
$ curl http://localhost:8000/v1/fund/NO0010062953/name
"ODIN Eiendom C"
```

```bash
$ curl http://localhost:8000/v1/fund/NO0010062953/currency
"NOK"
```

```bash
$ curl http://localhost:8000/v1/fund/NO0010062953/price
2144.52
```

or in Google Sheets:

```
=importdata("https://investapi.kradalby.no/v1/fund/NO0010062953/name")
```

```
=importdata("https://investapi.kradalby.no/v1/fund/NO0010062953/price")
```

or for stocks:

```bash
$ curl http://localhost:8000/v1/stock/AAPL/name
"Apple Inc."
```

```bash
$ curl http://localhost:8000/v1/stock/AAPL/currency
"USD"
```

```bash
$ curl http://localhost:8000/v1/stock/AAPL/price
142.52
```

## Development

Install with Poetry and start chipping away on the code!

Run the [Morningstar](https://www.morningstar.co.uk/uk/) tests with:

```bash
poetry run python morningstar_test.py
```
