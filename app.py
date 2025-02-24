from flask import Flask
from routes.main_routes import main_bp
from routes.download_routes import download_bp

app = Flask(__name__, static_folder='static')

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(download_bp)

if __name__ == "__main__":
    app.run(debug=False)