#!/usr/bin/env python3
import numpy as np

# The circle class used to construct the hierarchy graph of different circles in one ego network
class Circle:
    def __init__(self, circle_id , member_list):
        self.id = circle_id
        self.members = set(member_list)
        self.parents = set()
        self.children = set()
        self.depth = None # The depth of the set in the super set graph (a dag)
    
if __name__ == "__main__":
    path = "../../data/facebook/"
    user_id = 698
    filename_circle = "{0}{1}.circles".format(path, user_id)
    
    with open(filename_circle) as f:
        lines_str = f.read().splitlines()
        
    lines_str = [line.split('\t') for line in lines_str]
    lines_num = [list(map(int, [line[0][6:]] + line[1:])) for line in lines_str]
    circles = [Circle(line[0], line[1:]) for line in lines_num]
    
    n_cricle = len(circles)
        
    
    

