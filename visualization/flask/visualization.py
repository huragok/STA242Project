from flask import Flask, url_for
from flask import render_template, request
import os
import visualization_util

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 
    
@app.route('/user', methods=['POST'])
def user():
    return render_template('visualization.html', userID=request.form['userID'])
    
@app.route('/execute', methods=['POST'])
def execute():
  
    # Run the algorithm on the server, generate the json file and return
    userID = request.form['userID']
    K = request.form['K']
    path = "./static/"
    
    filename_out = "{0}_{1}.out".format(userID, K)
    print("{0}{1}".format(path, filename_out))
    if not os.path.isfile("{0}{1}".format(path, filename_out)): # Execute the community detection algorithm only when the output file does not exist.
        os.system("{0}cluster {0}facebook/{1} {2} {0}{3}".format(path, userID, K, filename_out))
    
    with open("{0}{1}".format(path, filename_out)) as f:
        lines_str = f.read().splitlines()
    
    circles_str = lines_str[5][13 : -2].split("],[")
    circle_members = [list(map(int, circle_str.split(','))) for circle_str in circles_str]
    file_edge = "{0}facebook/{1}.edges".format(path, userID)
    file_hierarchy = "{0}{1}_{2}.hierarchy.json".format(path, userID, K)
    file_ego = "{0}{1}_{2}.ego.json".format(path, userID, K)

    n = visualization_util.output_plot_json(circle_members, file_edge, file_hierarchy, file_ego, userID)
    
    return render_template('visualization.html', userID=request.form['userID'], K=K)

if __name__ == '__main__':
    app.run(debug=True)
