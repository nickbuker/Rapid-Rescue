from flask import Flask, render_template, request
app = Flask(__name__)

# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# home page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    user_data = request.data
    return render_template('predict.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/me')
def me():
    return render_template('me.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Be careful with debug!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
