import polygon, sqlite3, time
from credentials import polygon_api_key

print('''
************************************************
*                 WARNING!!!                   *
*    This script will take more than 4min to   *
*       complete. Please run with caution.     *
************************************************
''')
# Thought to make data collection and api key management part of the website too.
# But no one likes to stare at a loading screen for 5min just to get the data.


###################################################################################
# Change the below parameters as required to update the dataset
tickers = ['AAPL', 'NVDA', 'MSFT', 'AMZN']
multiplier = 5
timespan = 'minute'
from_ = '2024-01-01'
to_ = '2024-12-10'


schema = '''
    CREATE TABLE IF NOT EXISTS msft(timestamp_ INTEGER, open_ NUMERIC, close_ NUMERIC, high_ NUMERIC, low_ NUMERIC);
    CREATE TABLE IF NOT EXISTS amzn(timestamp_ INTEGER, open_ NUMERIC, close_ NUMERIC, high_ NUMERIC, low_ NUMERIC);
    CREATE TABLE IF NOT EXISTS aapl(timestamp_ INTEGER, open_ NUMERIC, close_ NUMERIC, high_ NUMERIC, low_ NUMERIC);
    CREATE TABLE IF NOT EXISTS nvda(timestamp_ INTEGER, open_ NUMERIC, close_ NUMERIC, high_ NUMERIC, low_ NUMERIC);
'''

client = polygon.RESTClient(polygon_api_key)

with sqlite3.connect('database.db') as conn:
    cur = conn.cursor()
    cur.executescript(schema)
    conn.commit()
    for ticker in tickers:
        print(f'Collecting {ticker}')
        data_count = 0
        try: 
            for row in client.list_aggs(ticker, multiplier, timespan, from_, to_, True, 'desc', 50000):
                entry = (row.timestamp//1000,row.open,row.close,row.high,row.low)
                cur.execute(f'INSERT INTO {ticker.lower()} VALUES(?, ?, ?, ?, ?)', entry)
                data_count += 1
            print(f'Fetched {data_count} Entries for {ticker}')
        except Exception as e:
            print(e)
        finally:
            conn.commit()
        if ticker != tickers[-1]:
            time.sleep(60) # Yes, this is necessary due to that damn API calls limit.
