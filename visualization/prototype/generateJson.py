#!/usr/bin/env python
import numpy as np
import json

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
    #FIXME remove identical circles
    member_id = {tuple(line[1:]): idx for idx, line in enumerate(lines_num)}
    
    circles = [Circle(idx, list(member)) for member, idx in member_id.items()]
    
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
            
    # Write the circle hierarchical DAG into a json file
    edges = [dict(s=circles[i_circle].id, d=child) for i_circle in range(n_circle - 1) for child in circles[i_circle].children]
    vertices = {circles[i_circle].id: {"description": '{0} users: '.format(len(circles[i_circle].members)) + ', '.join(str(x) for x in circles[i_circle].members)} for i_circle in range(n_circle)}
    data ={"user": user_id, "vertices": vertices, "edges": edges}
    filename = "{0}.hierarchy.json".format(user_id)
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
        
    # Generate the ego network
    users = dict()
    [Circle(idx, line[1:]) for idx, line in enumerate(lines_num)]
    for circle in circles:
        for user in circle.members:
            users.setdefault(user, set()).add(circle.id)
    print(len(users))
            
    filename_link = "{0}{1}.edges".format(path, user_id)
    with open(filename_link) as f:
        lines_str = f.read().splitlines()
        
    lines_str = [line.split(' ') for line in lines_str]
    links_raw = list({tuple(map(int, line)) for line in lines_str})
    for link in links_raw: # Add the rest of the users in the ego network even if they are not in any circle
        users.setdefault(link[0], set([-1,]))
        users.setdefault(link[1], set([-1,]))
    print(len(users))
    #print(users[2283])
    
    
    circle_map = {circle.id: circle for circle in circles}
    for user, user_circles in users.items(): # if a user is in set A and set A is a subset of set B, then we don't say this user is in set B
        circle_to_remove = set()
        for circle_sub in user_circles:
            for circle_sup in user_circles:
                if circle_sub != circle_sup and circle_sub > 0 and (circle_sup in circle_map[circle_sub].parents):
                    circle_to_remove.add(circle_sup)
                    
        users[user] -= circle_to_remove
        
    # Convert the circles that a user belong to into a tuple and count the number of circles it belong to
    users = {key: tuple(value) for key, value in users.items()}
    
    group_map = {circles: idx for idx, circles in enumerate(list(circle_map.keys()) + [-1,])}
    
    nodes = [dict(name = key, group = group_map[value[0]], ncircle = len(value), circles = [circle for circle in value if circle != -1], groups = [group_map[circle] for circle in value]) for key, value in users.items()]
    
    user_map = {value: key for key, value in enumerate(users.keys())}
    links = [dict(source = user_map[link[0]], target = user_map[link[1]], value = 1) for link in links_raw]
    
    filename = "{0}.ego.json".format(user_id)
    with open(filename, 'w') as outfile:
        json.dump({"nodes": nodes, "links": links}, outfile, indent=2)
    
        
   
 
    

