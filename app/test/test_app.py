from flask import Flask, render_template, request
app = Flask(__name__)

# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('test.html')

# home page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    user_data = request.data
    print user_data
    return render_template('predict.html')

# Be careful with debug!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
