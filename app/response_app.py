from flask import Flask, render_template
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html', title='Rapid Rescue')

# home page
@app.route('/predict')
def predict():
    pass

@app.route('/model')
def model():
    return render_template('model.html', title='Rapid Rescue')

@app.route('/me')
def me():
    return render_template('me.html', title='Rapid Rescue')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Rapid Rescue')

# Be careful with debug!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
