from flask import Flask, render_template, request, jsonify
from Poisson import PoissonModel
from allocation import allocator
from hist_retrieval import hist_retriever
from allocation import allocator
from clustering import clusterer
from itertools import chain
import cPickle as pickle
from ast import literal_eval
import time
import pandas as pd
import matplotlib.pyplot as plt


app = Flask(__name__)


# Set up some data
df = pd.read_csv('../data/seattle_911_prepped_no_out.csv', low_memory=False)
df.drop(['Unnamed: 0'], axis=1, inplace=True)
# Load pickled Poisson model
with open('PoissonModel.pkl', 'rb') as pkl_object:
    poisson_model = pickle.load(pkl_object)


# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# home page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Get user data
    user_data = request.data
    user_data = literal_eval(user_data)
    # Make predicton with Poisson model and allocate resources to zones
    preds = poisson_model.predict(user_data)
    alloc = allocator(user_data["num_units"], preds)
    # Get historical DataFrames
    df1,df2,df3,df4,df5,df6,df7 = _get_history(df, user_data)
    # Perform clustering to obtain centroids
    centroids = get_centroids(df1, df2, df3, df4, df5, df6, df7, alloc)
    # Make DataFrame from centroids
    centroid_df = _make_centroid_df(centroids)
    table = _make_table(centroid_df)
    img_name = _make_plot(df1, df2, df3, df4, df5, df6, df7,
                          centroid_df, user_data)
    return jsonify({'table':table, 'img_name':img_name})

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/me')
def me():
    return render_template('me.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


def _make_centroid_df(centroids):
    # Convert list of tuples into DataFrame
    centroid_df = pd.DataFrame(centroids)
    centroid_df.columns = ['Latitude', 'Longitude']
    centroid_df.index += 1
    return centroid_df


def _make_table(centroid_df):
    # Generate html code for table from centroid_df
    table = centroid_df.to_html()
    table.replace("\n", "")
    return table


def _get_history(df, query):
    # Set get home game info from user_data
    mariners, seahawks, sounders = 0,0,0
    if query['home_game'] == 'mariners':
        mariners = 1
    if query['home_game'] == 'seahawks':
        seahawks = 1
    if query['home_game'] == 'sounders':
        sounders = 1
    # Create History DataFrames for each zone
    df1 = hist_retriever(df, mariners, seahawks, sounders, query['date_input'],
                             query['time_range'], 'zone1')
    df2 = hist_retriever(df, mariners, seahawks, sounders, query['date_input'],
                             query['time_range'], 'zone2')
    df3 = hist_retriever(df, mariners, seahawks, sounders, query['date_input'],
                             query['time_range'], 'zone3')
    df4 =  hist_retriever(df, mariners, seahawks, sounders, query['date_input'],
                             query['time_range'], 'zone4')
    df5 =  hist_retriever(df, mariners, seahawks, sounders, query['date_input'],
                             query['time_range'], 'zone5')
    df6 = hist_retriever(df, mariners, seahawks, sounders, query['date_input'],
                             query['time_range'], 'zone6')
    df7 =  hist_retriever(df, mariners, seahawks, sounders, query['date_input'],
                             query['time_range'], 'zone7')
    return df1, df2, df3, df4, df5, df6, df7


def get_centroids(df1, df2, df3, df4, df5, df6, df7, alloc):
    # Find centroids with clusterer
    centroids1, clusters1 = clusterer(df1, int(alloc['zone1']))
    centroids2, clusters2 = clusterer(df2, int(alloc['zone2']))
    centroids3, clusters3 = clusterer(df3, int(alloc['zone3']))
    centroids4, clusters4 = clusterer(df4, int(alloc['zone4']))
    centroids5, clusters5 = clusterer(df5, int(alloc['zone5']))
    centroids6, clusters6 = clusterer(df6, int(alloc['zone6']))
    centroids7, clusters7 = clusterer(df7, int(alloc['zone7']))
    # Combine centroids and create DataFrame of locations
    centroids = list(chain(centroids1, centroids2, centroids3, centroids4,
                           centroids5, centroids6, centroids7))
    return centroids


def _make_plot(df1, df2, df3, df4, df5, df6, df7, centroid_df, user_data):
    # Plot historical data against optimal unit placements
    plt.figure(figsize=(8.5,12.5))
    # Limit points for speed of plotting
    if len(df1) > 1000:
        df1 = df1.sample(n=1000, random_state=42)
    plt.scatter(x=df1.Longitude, y=df1.Latitude, color='m', s=15, alpha=0.34)
    if len(df2) > 1000:
        df2 = df2.sample(n=1000, random_state=42)
    plt.scatter(x=df2.Longitude, y=df2.Latitude, color='orange', s=15, alpha=0.34)
    if len(df3) > 1000:
        df3 = df3.sample(n=1000, random_state=42)
    plt.scatter(x=df3.Longitude, y=df3.Latitude, color='#38d159', s=15, alpha=0.34)
    if len(df4) > 1000:
        df4 = df4.sample(n=1000, random_state=42)
    plt.scatter(x=df4.Longitude, y=df4.Latitude, color='b', s=15, alpha=0.34)
    if len(df5) > 1000:
        df5 = df5.sample(n=1000, random_state=42)
    plt.scatter(x=df5.Longitude, y=df5.Latitude, color='r', s=15, alpha=0.34)
    if len(df6) > 1000:
        df6 = df6.sample(n=1000, random_state=42)
    plt.scatter(x=df6.Longitude, y=df6.Latitude, color='#53cfd6', s=15, alpha=0.34)
    if len(df7) > 1000:
        df7 = df7.sample(n=1000, random_state=42)
    plt.scatter(x=df7.Longitude, y=df7.Latitude, color='#868591', s=15, alpha=0.34)
    plt.scatter(centroid_df.Longitude, centroid_df.Latitude, s=150, color='k')
    plt.xlabel('Longitude', fontsize=20, fontweight='bold')
    plt.ylabel('Latitude', fontsize=20, fontweight='bold')
    plt.title('Seattle 911 Responses by Zone', fontsize=24, fontweight='bold')
    plt.legend(['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6', 'Zone 7', 'Units'], fontsize=12)
    ts = str(time.time())
    plt.savefig('../app/static/zseattle'+ ts +'.png')
    return 'zseattle'+ ts +'.png'


# Be careful with debug!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
