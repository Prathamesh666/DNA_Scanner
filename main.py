from flask import Flask, render_template
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'   # disables oneDNN optimizations
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'   # suppress INFO and WARNING logs
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from routes.detect import detect_route

app = Flask(__name__)
app.register_blueprint(detect_route)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)