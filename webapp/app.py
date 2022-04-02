import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from flask import Flask, flash, redirect, render_template, request, session, abort
import customer_individual_pricing as CIP
 
app = Flask(__name__)

@app.route('/')
def index():    
    return render_template('input.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
	# All these try-except statements are to make sure entries are input correctly.
		try:
			keyphrase = str(request.form['keyphrase'])
			try:
			    print(keyphrase)
								
			except Exception as e:
				print(e)
				return 'Analysis failed!'
		except:
			return 'Incorrect input for key phrase!'
 
if __name__ == "__main__":
#	app.debug = True
	app.run(host='127.0.0.1', port=8888, debug=True)
