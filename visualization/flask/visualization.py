from flask import Flask, url_for
from flask import render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 
    
@app.route('/user', methods=['POST'])
def user():
    return render_template('visualization.html', userID=request.form['userID']) 
    
if __name__ == '__main__':
    app.run(debug=True)
