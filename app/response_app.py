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

# Be careful with debug!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
