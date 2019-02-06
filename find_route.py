import sys

class Node:
    def __init__(self):
        self.distance = 0
        self.parent = None
        self.city = ''


# creates dictionary links with (source, destination) as key and cost as value
def create_links(input_file):
    dict_links = {}
    input_file_content = open(input_file, 'r')
    for line in input_file_content:
        line = line.rstrip()
        if line == 'END OF INPUT':
            break
        source, destination, cost = line.split(' ')
        dict_links[source, destination] = int(cost)
    input_file_content.close()
    return dict_links


# gets the neighbours of source
def get_neighbours(source, dict_links):
    neighbours = []
    for src, dest in dict_links.keys():
        if src == source:
            neighbours.append(dest)
        if dest == source:
            neighbours.append(src)
    return neighbours


# display route from goal to source then reverses it
def display_route(source, dict_links):
    path = []
    while source.parent:
        if (source.city, source.parent.city) in dict_links:
            path.append([source.city, source.parent.city, dict_links[source.city, source.parent.city]])
        else:
            path.append([source.parent.city, source.city, dict_links[source.parent.city, source.city]])
        source = source.parent
    path.reverse()
    for source_city, destination_city, distance in path:
        print(source_city + " to " + destination_city + ', ' + str(distance) + ' km')


def uniform_cost_search(links, src, dest):
    source = Node()
    fringe = [(src, 0, None)]
    visited = []
    path_found = False
    expanded_nodes = 0
    
    # while fringe is not empty
    while fringe:
        # track number of nodes expanded
        expanded_nodes += 1
        fringe_first, d, parent = fringe.pop(0)
        # if node is already is visited then skip the node
        if fringe_first in visited:
            continue
        temp_node = Node()
        source = parent
        if fringe_first == src:
            # if node is source node then distance between them is 0
            temp_node.distance = 0
        elif (fringe_first, source.city) in dict_links:
            # calculates distance between fringe_first and source
            temp_node.distance = source.distance + dict_links[fringe_first, source.city]
        elif (source.city, fringe_first) in dict_links:
            # calculates distance between fringe_first and source
            temp_node.distance = source.distance + dict_links[source.city, fringe_first]
        else:
            continue
        temp_node.parent = source
        temp_node.city = fringe_first
        visited.append(fringe_first)
        if fringe_first == dest:
            # Path found and displayed distance
            print('nodes expanded: ' + str(expanded_nodes))
            print('distance: ' + str(temp_node.distance) + ' km')
            print('route:')
            # Path from end node to start then reversed
            display_route(temp_node, dict_links)
            path_found = True
            break
        # gets neighbours of fringe first
        successors = get_neighbours(fringe_first, dict_links)
        # for every successor, calculate distance and add in fringe
        for successor in successors:
            successor_node = Node()
            successor_node.city = successor
            successor_node.parent = temp_node
            if (temp_node.city, successor) in dict_links:
                successor_node.distance = temp_node.distance + dict_links[temp_node.city, successor]
            elif (successor, temp_node.city) in dict_links:
                successor_node.distance = temp_node.distance + dict_links[successor, temp_node.city]
            fringe.append((successor_node.city, successor_node.distance, temp_node))
        fringe.sort(key=lambda val: val[1])
    if not path_found:
        print('nodes expanded: ' + str(expanded_nodes))
        print('distance: infinity')
        print('route:\nnone')


if __name__ == '__main__':
    program_file, input_file, source, destination = sys.argv
    dict_links = create_links(input_file)
    uniform_cost_search(dict_links, source, destination)
