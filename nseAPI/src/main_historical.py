from webscraper.security_historical import HistoricalData
from webscraper.security_historical import AvailableSecurities

avail = AvailableSecurities()

symbols = avail.get_available_securities(columns=['SYMBOL'], series='EQ')

# Re arrange symbol list
symbols = [x[0] for x in symbols]

print("All symbol length: " ,len(symbols))
hist = HistoricalData()

hist.create_table_for_securities(symbols)

for index, symbol in enumerate(symbols):
    print(f"Security #{index + 1}: {symbol}")
    df = hist.get_data_for_security(symbol)
    hist.upsert_data(df)