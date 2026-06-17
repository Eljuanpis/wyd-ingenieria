import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index') 
def index():
    return render_template('index.html')

@app.route('/ingenieria')
def ingenieria():
    return render_template('ingenieria.html') 

@app.route('/montajes')
def montajes():
    return render_template('montajes.html') 

@app.route('/mecanica')
def mecanica():
    return render_template('mecanica.html')

@app.route('/metalmecanica')
def metalmecanica():
    return render_template('metalmecanica.html')

@app.route('/energia')
def energia():
    return render_template('energia.html')

@app.route('/construccion')
def construccion():
    return render_template('construccion.html')

if __name__ == '__main__':
    app.run(debug=True)