import pandas as pd

df = pd.read_csv(
    "dados/vendas.csv",
    parse_dates=["data"]
)
