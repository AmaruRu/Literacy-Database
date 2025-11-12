from flask import Flask, request, jsonify, redirect, url_for, render_template   # Import Flask and related modules
from flask_sqlalchemy import SQLAlchemy # Import SQLAlchemy for database interactions
from flask_login import LoginManager, current_user # Import LoginManager for user session management
import logging
import os # Import os for environment variable access
from dotenv import load_dotenv # Import load_dotenv to load environment variables from a .env file
from urllib.parse import quote_plus # Import quote_plus to safely encode database passwords in the URI

db = SQLAlchemy() # Initialize SQLAlchemy
login_manager = LoginManager()

def create_website(): # Function to create and configure the Flask app
    website = Flask(__name__)

    load_dotenv()

    website.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    website.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    website.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    website.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

    website.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://' + os.getenv("MYSQL_USER") + \
        ':' + quote_plus(os.getenv("MYSQL_PASSWORD")) + '@' + os.getenv("MYSQL_HOST") + '/' + os.getenv("MYSQL_DB") 
    # Configure SQLAlchemy database URI (uniform resource identifier); using PyMySQL driver for MySQL
    db.init_app(website)

    # Register API blueprints
    from .api import api_bp     
    website.register_blueprint(api_bp)  # Register the API blueprint with the Flask app

    with website.app_context(): # Ensure the app context is active for database operations
       from .models import User, Districts, Schools, Subgroups, PerformanceData, TeacherQuality, NAEPAssessments
       
       db.create_all()
       
       return website