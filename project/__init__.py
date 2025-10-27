from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import logging
import os
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()

def create_website():
    website = Flask(__name__)

    load_dotenv()

    website.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    website.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    website.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    website.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

    website.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://' + os.getenv("MYSQL_USER") + \
        ':' + os.getenv("MYSQL_PASSWORD") + '@' + os.getenv("MYSQL_HOST") + '/' + os.getenv("MYSQL_DB")
    
    db.init_app(website)

    with website.app_context():
       from .models import User
       
       db.create_all()
       
       return website