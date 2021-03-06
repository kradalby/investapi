"""
This type stub file was generated by pyright.
"""

class TickerBase:
    def __init__(self, ticker, session=...) -> None:
        ...
    
    def history(self, period=..., interval=..., start=..., end=..., prepost=..., actions=..., auto_adjust=..., back_adjust=..., proxy=..., rounding=..., tz=..., **kwargs):
        """
        :Parameters:
            period : str
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                Either Use period parameter or use start and end
            interval : str
                Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days
            start: str
                Download start date string (YYYY-MM-DD) or _datetime.
                Default is 1900-01-01
            end: str
                Download end date string (YYYY-MM-DD) or _datetime.
                Default is now
            prepost : bool
                Include Pre and Post market data in results?
                Default is False
            auto_adjust: bool
                Adjust all OHLC automatically? Default is True
            back_adjust: bool
                Back-adjusted data to mimic true historical prices
            proxy: str
                Optional. Proxy server URL scheme. Default is None
            rounding: bool
                Round values to 2 decimal places?
                Optional. Default is False = precision suggested by Yahoo!
            tz: str
                Optional timezone locale for dates.
                (default data is returned as non-localized dates)
            **kwargs: dict
                debug: bool
                    Optional. If passed as False, will suppress
                    error message printing to console.
        """
        ...
    
    def get_recommendations(self, proxy=..., as_dict=..., *args, **kwargs): # -> None:
        ...
    
    def get_calendar(self, proxy=..., as_dict=..., *args, **kwargs): # -> None:
        ...
    
    def get_major_holders(self, proxy=..., as_dict=..., *args, **kwargs): # -> None:
        ...
    
    def get_institutional_holders(self, proxy=..., as_dict=..., *args, **kwargs): # -> None:
        ...
    
    def get_mutualfund_holders(self, proxy=..., as_dict=..., *args, **kwargs): # -> None:
        ...
    
    def get_info(self, proxy=..., as_dict=..., *args, **kwargs): # -> dict[Unknown, Unknown] | None:
        ...
    
    def get_sustainability(self, proxy=..., as_dict=..., *args, **kwargs): # -> None:
        ...
    
    def get_earnings(self, proxy=..., as_dict=..., freq=...):
        ...
    
    def get_financials(self, proxy=..., as_dict=..., freq=...):
        ...
    
    def get_balancesheet(self, proxy=..., as_dict=..., freq=...):
        ...
    
    def get_balance_sheet(self, proxy=..., as_dict=..., freq=...):
        ...
    
    def get_cashflow(self, proxy=..., as_dict=..., freq=...):
        ...
    
    def get_dividends(self, proxy=...): # -> list[Unknown]:
        ...
    
    def get_splits(self, proxy=...): # -> list[Unknown]:
        ...
    
    def get_actions(self, proxy=...): # -> list[Unknown]:
        ...
    
    def get_isin(self, proxy=...): # -> str:
        ...
    


