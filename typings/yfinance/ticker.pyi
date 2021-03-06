"""
This type stub file was generated by pyright.
"""

from .base import TickerBase

class Ticker(TickerBase):
    def __repr__(self):
        ...
    
    def option_chain(self, date=..., proxy=..., tz=...): # -> Options:
        ...
    
    @property
    def isin(self): # -> str:
        ...
    
    @property
    def major_holders(self): # -> None:
        ...
    
    @property
    def institutional_holders(self): # -> None:
        ...
    
    @property
    def mutualfund_holders(self): # -> None:
        ...
    
    @property
    def dividends(self): # -> list[Unknown]:
        ...
    
    @property
    def splits(self): # -> list[Unknown]:
        ...
    
    @property
    def actions(self): # -> list[Unknown]:
        ...
    
    @property
    def info(self): # -> dict[Unknown, Unknown] | None:
        ...
    
    @property
    def calendar(self): # -> None:
        ...
    
    @property
    def recommendations(self): # -> None:
        ...
    
    @property
    def earnings(self):
        ...
    
    @property
    def quarterly_earnings(self):
        ...
    
    @property
    def financials(self):
        ...
    
    @property
    def quarterly_financials(self):
        ...
    
    @property
    def balance_sheet(self):
        ...
    
    @property
    def quarterly_balance_sheet(self):
        ...
    
    @property
    def balancesheet(self):
        ...
    
    @property
    def quarterly_balancesheet(self):
        ...
    
    @property
    def cashflow(self):
        ...
    
    @property
    def quarterly_cashflow(self):
        ...
    
    @property
    def sustainability(self): # -> None:
        ...
    
    @property
    def options(self): # -> tuple[Unknown, ...]:
        ...
    


