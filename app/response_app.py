from flask import Flask, render_template, request, jsonify
from hist_retrieval import hist_retriever
from ast import literal_eval
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Set up some data
df = pd.read_csv('../data/seattle_911_prepped_no_out.csv', low_memory=False)
df.drop(['Unnamed: 0'], axis=1, inplace=True)
centroids = [(47.677581272727238, -122.37939533192382),
             (47.712919741029665, -122.34805637909501),
             (47.664287271540537, -122.34211233420372),
             (47.681384914285708, -122.28977103214292),
             (47.663089380952385, -122.31089547368411),
             (47.714972091304404, -122.30650323260878),
             (47.623308516528915, -122.34742645867757),
             (47.639689687999997, -122.37474428799995),
             (47.652112489999993, -122.39818523999999),
             (47.64042387500001, -122.34223335156256),
             (47.613575095864661, -122.32143335526312),
             (47.599794525735298, -122.3026922132353),
             (47.62844241538459, -122.29922202051286),
             (47.614138608076018, -122.34659261757716),
             (47.601259945355217, -122.3308707909837),
             (47.611751771464697, -122.33686217929268),
             (47.534350779951097, -122.37410144743274),
             (47.570948721804541, -122.38625972431088),
             (47.525884480874325, -122.33938371038252),
             (47.552964609236263, -122.29280141563041),
             (47.521587190163949, -122.26989246557379),
             (47.583197496143995, -122.31985378663238)]


# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# home page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    user_data = request.data
    user_data = literal_eval(user_data)
    centroid_df = _make_centroid_df(centroids)
    table = _make_table(centroid_df)
    _make_plot(df, centroid_df, user_data)
    return jsonify({'table':table})

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
    centroid_df = pd.DataFrame(centroids)
    centroid_df.columns = ['Latitude', 'Longitude']
    centroid_df.index += 1
    return centroid_df


def _make_table(centroid_df):
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


def _make_plot(df, centroid_df, user_data):
    # Get historical DataFrames
    df1,df2,df3,df4,df5,df6,df7 = _get_history(df, user_data)
    # Plot historical data against optimal unit placements
    plt.figure(figsize=(16.96,25))
    plt.scatter(x=df1.Longitude, y=df1.Latitude, color='m', s=30, alpha=0.4)
    plt.scatter(x=df2.Longitude, y=df2.Latitude, color='orange', s=30, alpha=0.4)
    plt.scatter(x=df3.Longitude, y=df3.Latitude, color='#38d159', s=30, alpha=0.4)
    plt.scatter(x=df4.Longitude, y=df4.Latitude, color='b', s=30, alpha=0.4)
    plt.scatter(x=df5.Longitude, y=df5.Latitude, color='r', s=30, alpha=0.4)
    plt.scatter(x=df6.Longitude, y=df6.Latitude, color='#53cfd6', s=30, alpha=0.4)
    plt.scatter(x=df7.Longitude, y=df7.Latitude, color='#868591', s=30, alpha=0.4)
    plt.scatter(centroid_df.Longitude, centroid_df.Latitude, s=400, color='k')
    plt.xlabel('Longitude', fontsize=28, fontweight='bold')
    plt.ylabel('Latitude', fontsize=28, fontweight='bold')
    plt.title('Seattle 911 Responses by Zone', fontsize=36, fontweight='bold')
    plt.legend(['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6', 'Zone 7', 'Units'], fontsize=18)
    plt.savefig('../app/static/seattle_911_pred_live.png')
    print "plot function fired"


# Be careful with debug!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
