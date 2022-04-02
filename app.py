import warnings
warnings.filterwarnings('ignore')

from flask import Flask, flash, redirect, render_template, request, session, abort
from util import get_keyword_record_from_dynamodb

app = Flask(__name__)

@app.route('/')
def index():    
    return render_template('input.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    # All these try-except statements are to make sure entries are input correctly.
    try:
        keyphrase = request.form['keyphrase']
        try:
            return keyphrase
								
        except Exception as e:
            print(e)
            return 'Analysis failed!'
    except:
        return 'Incorrect input for key phrase!'
 
if __name__ == "__main__":
    app.run(port=8080, debug=True)
