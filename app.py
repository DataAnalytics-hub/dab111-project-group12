# Imports
from datetime import datetime, timezone
from flask import Flask, Response, g, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as Canvas
from matplotlib.figure import Figure
import matplotlib as mpl, matplotlib.pyplot as plt
import io, sqlite3, pandas as pd, seaborn as sns
plt.style.use('ggplot')
mpl.use('Agg')



# Application Setup
app = Flask(__name__)
app.config.setdefault('TICKERS', {
    'AAPL': 'Apple Inc. Stock Value in United States Dollar',
    'NVDA': 'Nvidia Corp. Stock Value in United States Dollar',
    'MSFT': 'Microsoft Corp. Stock Value in United States Dollar',
    'AMZN': 'Amazon.com Inc. Stock Value in United States Dollar',
})



# Database Handlers accross requests
def db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('./database.db').cursor()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.connection.close()



# Helper Functions
def get_dataset(ticker):
    data = db().execute(f'SELECT timestamp_, close_ FROM {ticker.lower()} ORDER BY timestamp_').fetchall()
    df = pd.DataFrame(data, columns=['timestamp', 'closing_price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return (app.config.get('TICKERS')[ticker], df)



# Route Handlers
@app.get('/')
@app.get('/about')
def about():
    g.nav_active = 'about'
    return render_template('about.html')

@app.get('/dataset')
def dataset():
    g.nav_active = 'dataset'
    datasets = dict()
    for ticker, desc in app.config['TICKERS'].items():
        data = db().execute(f'SELECT * FROM {ticker.lower()} ORDER BY timestamp_ DESC LIMIT 5').fetchall()
        data = list(map(lambda x: (datetime.fromtimestamp(x[0], timezone.utc).strftime('%Y-%m-%d %H:%M'), *x[1:]), data))
        count = db().execute(f'SELECT COUNT(*) FROM {ticker.lower()}').fetchone()[0]
        datasets[ticker] = {'data': data, 'count': count, 'description': desc}
    return render_template('dataset.html', datasets = datasets)

@app.get('/plots')
def plots():
    g.nav_active = 'plots'
    return render_template('visuals.html', names = app.config.get('TICKERS').keys())

@app.get('/plot/<string:idx>')
def plot(idx):
    fig = Figure((10, 6), dpi=120)
    ax = fig.add_subplot(1,1,1)
    desc, df = get_dataset(idx)
    sns.lineplot(df, x='timestamp', y='closing_price', linewidth=1, ax=ax)
    ax.set_title(desc)
    ax.set_xlabel('Timeline')
    ax.set_ylabel('Price ($)')
    buff = io.BytesIO()
    Canvas(fig).print_png(buff)
    return Response(buff.getvalue(), mimetype='image/png')


# Development run using normal script execution
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=3300)