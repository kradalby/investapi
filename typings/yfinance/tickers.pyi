"""
This type stub file was generated by pyright.
"""

class Tickers:
    def __repr__(self): # -> str:
        ...
    
    def __init__(self, tickers) -> None:
        ...
    
    def history(self, period=..., interval=..., start=..., end=..., prepost=..., actions=..., auto_adjust=..., proxy=..., threads=..., group_by=..., progress=..., **kwargs):
        ...
    
    def download(self, period=..., interval=..., start=..., end=..., prepost=..., actions=..., auto_adjust=..., proxy=..., threads=..., group_by=..., progress=..., **kwargs):
        ...
    


