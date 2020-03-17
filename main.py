from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/messaging_templates')
def messaging_templates():
	return render_template('messaging_templates.html')