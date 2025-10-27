from flask import Flask, request, jsonify, url_for, render_template
from MS_Lit.project import create_website

website = create_website()

@website.route('/', methods = ['GET'])
def home():
    return jsonify(("Welcome to Mississippi Literacy"))

@website.route('/mission', methods = ['GET'])
def mission():
    return render_template('index.html')

@website.route('/books', methods = ['GET'])
def books():
    return jsonify(("Book Exploration in Mississippi"))

if __name__ == '__main__':
    website.run(debug = True)