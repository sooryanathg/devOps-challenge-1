from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Flask DevOps Challenge!',
        'status': 'success',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'flask-app'
    }), 200

@app.route('/about')
def about():
    return jsonify({
        'app': 'DevOps Challenge Flask App',
        'description': 'A simple Flask application for CI/CD demonstration',
        'author': 'DevOps Student'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
