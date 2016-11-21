from flask import Flask, render_template, request, jsonify
import pandas as pd
app = Flask(__name__)

# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# home page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    user_data = request.data
    print user_data
    table = make_table(centroids)
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

def make_table(centroids):
    centroid_df = pd.DataFrame(centroids)
    centroid_df.columns = ['Latitude', 'Longitude']
    centroid_df.index += 1
    table = centroid_df.to_html()
    table.replace("\n", "")
    return table


# Be careful with debug!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
