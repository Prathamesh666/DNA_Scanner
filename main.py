import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'   # disables oneDNN optimizations
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'   # suppress INFO and WARNING logs
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'   # force CPU, no GPU warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'   # suppress INFO, WARNING, ERROR logs
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from flask import Flask, render_template, send_from_directory
from routes.detect import detect_route

app = Flask(__name__)
app.register_blueprint(detect_route)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.dirname(__file__), 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.dirname(__file__), 'robots.txt', mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))              # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port, debug=False)
    #app.run(host="0.0.0.0", port=443, ssl_context=("/etc/ssl/certs/dna-scanner.crt", "/etc/ssl/private/dna-scanner.key"))
    #app.run(debug=True)