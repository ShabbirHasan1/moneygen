from webscraper.security_historical import HistoricalData
from webscraper.security_historical import AvailableSecurities

# avail = AvailableSecurities()

# symbols = avail.get_available_securities(columns=['SYMBOL'], series='EQ')

# Re arrange symbol list
# TODO: Handle special cases in data like 'GET&D', symbol name in CSV is inconsistent, code might break due to special char
symbols = ['TEXRAIL', 'TFCILTD', 'TFL', 'TGBHOTELS', 'THANGAMAYL', 'THEINVEST', 'THERMAX', 'THOMASCOOK', 'THYROCARE', 'TI', 'TIDEWATER', 'TIIL', 'TIINDIA', 'TIJARIA', 'TIL', 'TIMESGTY', 'TIMETECHNO', 'TIMKEN', 'TINPLATE', 'TIPSINDLTD', 'TIRUMALCHM', 'TITAN', 'TNPETRO', 'TNPL', 'TOKYOPLAST', 'TORNTPHARM', 'TORNTPOWER', 'TOUCHWOOD', 'TPLPLASTEH', 'TREEHOUSE', 'TRENT', 'TRIDENT', 'TRIGYN', 'TRIL', 'TRITURBINE', 'TRIVENI', 'TTKHLTCARE', 'TTKPRESTIG', 'TTL', 'TV18BRDCST', 'TVSELECT', 'TVSMOTOR', 'TVSSRICHAK', 'TVTODAY', 'TWL', 'UBL', 'UCALFUEL', 'UCOBANK', 'UFLEX', 'UFO', 'UGARSUGAR', 'UJAAS', 'UJJIVAN', 'UJJIVANSFB', 'ULTRACEMCO', 'UMANGDAIRY', 'UNICHEMLAB', 'UNIENTER', 'UNIONBANK', 'UNIPLY', 'UNITEDTEA', 'UNIVCABLES', 'UNIVPHOTO', 'UPL', 'USHAMART', 'UTTAMSUGAR', 'V2RETAIL', 'VADILALIND', 'VAIBHAVGBL', 'VAISHALI', 'VAKRANGEE', 'VARDHACRLC', 'VARROC', 'VASCONEQ', 'VASWANI', 'VBL', 'VEDL', 'VENKEYS', 'VESUVIUS', 'VETO', 'VGUARD', 'VHL', 'VIDHIING', 'VIJIFIN', 'VIKASECO', 'VIKASPROP', 'VIKASWSP', 'VIMTALABS', 'VINATIORGA', 'VINDHYATEL', 'VINYLINDIA', 'VIPCLOTHNG', 'VIPIND', 'VIPULLTD', 'VISAKAIND', 'VISHNU', 'VISHWARAJ', 'VIVIDHA', 'VLSFINANCE', 'VMART', 'VOLTAMP', 'VOLTAS', 'VRLLOG', 'VSSL', 'VSTIND', 'VSTTILLERS', 'VTL', 'WABAG', 'WABCOINDIA', 'WATERBASE', 'WEIZMANIND', 'WELCORP', 'WELENT', 'WELINV', 'WELSPUNIND', 'WENDT', 'WESTLIFE', 'WHEELS', 'WHIRLPOOL', 'WILLAMAGOR', 'WIPRO', 'WOCKPHARMA', 'WONDERLA', 'WSTCSTPAPR', 'XCHANGING', 'XELPMOC', 'XPROINDIA', 'YESBANK', 'ZEEL', 'ZEELEARN', 'ZENITHEXPO', 'ZENSARTECH', 'ZENTEC', 'ZICOM', 'ZODIACLOTH', 'ZODJRDMKJ', 'ZOTA', 'ZUARIGLOB', 'ZYDUSWELL']
print(len(symbols))
hist = HistoricalData()

# hist.create_table_for_securities(symbols)

for index, symbol in enumerate(symbols):
    print(f"Security #{index + 1}: {symbol}")
    df = hist.get_data_for_security(symbol)
    hist.upsert_data(df, symbol)