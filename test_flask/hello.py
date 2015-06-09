from flask import Flask, url_for
from flask import render_template
app = Flask(__name__)

@app.route('/user/')
@app.route('/user/<userID>')
def user(userID = 698):
    return render_template('visualization.html', userID=userID) 
    
if __name__ == '__main__':
    app.run(debug=True)
