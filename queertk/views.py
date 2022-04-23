from flask import render_template
from queertk import app

@app.route('/')
def home():

    return render_template('index.html', title = 'Home')