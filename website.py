from flask import render_template
from project import create_website
import webbrowser

website = create_website()

webbrowser.open('http://127.0.0.1:5000/')

@website.route('/', methods = ['GET'])
def home():
    return render_template('layout.html')

@website.route('/mission.html', methods = ['GET'])
def mission():
    return render_template('mission.html')

@website.route('/books.html', methods = ['GET'])
def books():
    return render_template('books.html')

@website.route('/map.html', methods = ['GET'])
def map_page():
    return render_template('map.html')

@website.route('/dashboard.html', methods = ['GET'])
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    website.run(debug = True)