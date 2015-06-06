#!/usr/bin/env python
import numpy as np
import xml.etree.cElementTree as ET

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
    circles = [Circle(idx, line[1:]) for idx, line in enumerate(lines_num)]
    
    n_circle = len(circles)
    flag_ancestor = np.zeros((n_circle, n_circle), dtype=np.int) # If the i-th circle is a superset of the j-th circle, then we call circle i is an ancector of j or j is an offspring of i. Correspondingly, we set flag_ancestor[i, j] = 1 and flag_ancestor[j, i] = -1. Otherwise, flag_ancestor[i, j] = flag_ancestor[j, i]  = 0
    list_ancestor = [list() for i_circle in range(n_circle)]
    for i_circle in range(n_circle - 1):
        for j_circle in range(i_circle + 1, n_circle):
            if circles[i_circle].members >= circles[j_circle].members:
                flag_ancestor[i_circle, j_circle] = 1
                flag_ancestor[j_circle, i_circle] = -1
                list_ancestor[j_circle].append(i_circle)
            elif circles[i_circle].members <= circles[j_circle].members:
                flag_ancestor[i_circle, j_circle] = -1
                flag_ancestor[j_circle, i_circle] = 1
                list_ancestor[i_circle].append(j_circle)
                
    
    # If circle M is a superset of circle N and there is no circle that is both a subset of M and a super set of N, than we call M is a parent of N and N is a child of M. Next we figure out the parental relationship between all circles
    for i_circle in range(n_circle):
        for ancestor in list_ancestor[i_circle]:
            # Check all other ancestors of i_circle
            ancestor_rest = [a for a in list_ancestor[i_circle] if a != ancestor]
            if not(np.any(flag_ancestor[ancestor, ancestor_rest] == 1)): 
                circles[i_circle].parents.add(circles[ancestor].id)
                circles[ancestor].children.add(circles[i_circle].id)
               
    
    # Write the circle hierarchical DAG into a xml file
    root = ET.Element("dag")
    vertices = ET.SubElement(root, "vertices")
    edges = ET.SubElement(root, "edges")
    for i_circle in range(n_circle - 1):
        ET.SubElement(vertices, "vertex").text = str(i_circle)
        for child in circles[i_circle].children:
            edge = ET.SubElement(edges, "edge")
            ET.SubElement(edge, "s").text = str(i_circle)
            ET.SubElement(edge, "d").text = str(child)
    tree = ET.ElementTree(root)
    filename = "{0}.hierarchy.xml".format(user_id)
    tree.write(filename)
    
    
    
    

