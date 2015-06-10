UC Davis 2015 Spring STA 242 Statistical Programming Project - Visualization

This directory contains the prototype and a flask application for the visualization of the Facebook data for community detection in "Learning to discover social circles in ego networks". A detailed description can be found in our project's webpages.

The structure of this repository is as follows:
1. "./code/": the c++ code for the community detection, which is modified from 
2. "./data/": the original data
3. "./visualization/:" the project's main directory, where in "./visualization/prototype" we test the design of the data processing and visualization, and in "./visualization/flask" we integrate them into a small flask project.

To run the flask application one can follow the following steps:
1. compile the c++ code in "./code/", copy the executable "cluster" into "./visualization/flask/static/"
2. Install flask as per http://flask.pocoo.org/docs/0.10/installation/
3. Change into directory "./visualization/flask".
4. run "python visualization.py" to start a server
5. Open a browser and head over to the url (http://127.0.0.1:5000/ by default) and have fun!

We highly recommend using Chrome browser by which the dynamic/interactive visulization requires intensive computation could be better handled. 
