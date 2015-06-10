import numpy as np
import json
import random

# The circle class used to construct the hierarchy graph of different circles in one ego network
class Circle:
    def __init__(self, circle_id , member_list):
        self.id = circle_id
        self.members = set(member_list)
        self.parents = set()
        self.children = set()
        self.depth = None # The depth of the set in the super set graph (a dag)

# The function to output hierarchy and ego json files given a list of cirles
def output_plot_json(circle_members, file_edge, file_hierarchy, file_ego, user_id):
    circles = [Circle(idx, list(member)) for idx, member in enumerate(circle_members)]
    n_circle = len(circles)
    flag_ancestor = np.zeros((n_circle, n_circle), dtype=np.int)
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
                
    for i_circle in range(n_circle):
        for ancestor in list_ancestor[i_circle]:
            # Check all other ancestors of i_circle
            ancestor_rest = [a for a in list_ancestor[i_circle] if a != ancestor]
            if not(np.any(flag_ancestor[ancestor, ancestor_rest] == 1)): 
                circles[i_circle].parents.add(circles[ancestor].id)
                circles[ancestor].children.add(circles[i_circle].id)
    
    circle_map = {circle.id: circle for circle in circles}
    group_map = {circles: idx for idx, circles in enumerate(list(circle_map.keys()) + [-1,])}
    
    # Write the circle hierarchical DAG into a json file
    edges = [dict(s=circles[i_circle].id, d=child) for i_circle in range(n_circle - 1) for child in circles[i_circle].children]
    vertices = {circles[i_circle].id: {"description": '{0} users: '.format(len(circles[i_circle].members)) + ', '.join(str(x) for x in circles[i_circle].members), "group": group_map[circles[i_circle].id]} for i_circle in range(n_circle)}
    data ={"user": user_id, "vertices": vertices, "edges": edges}
    with open(file_hierarchy, 'w') as outfile:
        json.dump(data, outfile)
        
    # Generate the ego network
    users = dict()
    for circle in circles:
        for user in circle.members:
            users.setdefault(user, set()).add(circle.id)
    
    with open(file_edge) as f:
        lines_str = f.read().splitlines()
    
    lines_str = [line.split(' ') for line in lines_str]
    links_raw = list({tuple(map(int, line)) for line in lines_str})
    for link in links_raw: # Add the rest of the users in the ego network even if they are not in any circle
        users.setdefault(link[0], set([-1,]))
        users.setdefault(link[1], set([-1,]))

    users = {key: tuple(value) for key, value in users.items()}    
    nodes = [dict(name = key, group = group_map[random.choice(value)], circles = [circle for circle in value if circle != -1], groups = [group_map[circle] for circle in value]) for key, value in users.items()]
    
    user_map = {value: key for key, value in enumerate(users.keys())}
    links = [dict(source = user_map[link[0]], target = user_map[link[1]], value = 1) for link in links_raw]
    with open(file_ego, 'w') as outfile:
        json.dump({"nodes": nodes, "links": links, "ncircle": n_circle, "nuser": len(users)}, outfile, indent=2)
        
    return (n_circle)
