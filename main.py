from sapp import app
import os

if __name__ == '__main__':
    print("Starting Flask application...")
    # Use environment variable for port, default to 5001 for local dev
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '127.0.0.1')
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(debug=debug, host=host, port=port)
