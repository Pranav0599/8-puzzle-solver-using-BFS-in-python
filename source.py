import numpy as np
#Creating Node  class
class Node:
  def __init__(self, state, node_key, parent_key, cost2come):
      self.node_key = node_key
      self.state = state
      self.parent_key = parent_key
      self.cost2come = cost2come

def fetch_node_val(node):
  if type(node) == int:
    for k,n in node_book.items():
      return n
  if type(node) == np.ndarray:
    for k,n in node_book.items():
      return n

  else:
    return node

#   Locating the blank tile which is '0' int the matrix
def locate_zero(current_state):
  return np.where(current_state == 0)[0][0], np.where(current_state == 0)[1][0]

#Creating functions to move the blank tile
def move_up(state):

    i,j = locate_zero(state)
    new_i, new_j = i-1, j

    if new_i >= 0 and new_i < 3:    
        new_puzz_state = state.copy()
        new_puzz_state[i,j] = state[new_i,new_j]
        new_puzz_state[new_i, new_j] = 0
        return new_puzz_state

    return False

def move_down(state):
    i,j = locate_zero(state)
    new_i, new_j = i+1, j

    if new_i >= 0 and new_i < 3:
        new_puzz_state = state.copy()
        new_puzz_state[i,j] = state[new_i,new_j]
        new_puzz_state[new_i, new_j] = 0
        pos_zero = (i,j)
        return new_puzz_state
    return False


def move_left(state):
    i,j = locate_zero(state)
    new_i, new_j = i, j-1

    if new_j >= 0 and new_j < 3:
        new_puzz_state = state.copy()
        new_puzz_state[i,j] = state[new_i,new_j]
        new_puzz_state[new_i, new_j] = 0
        pos_zero = (i,j)
        return new_puzz_state
    return False


def move_right(state):
    i,j = locate_zero(state)
    new_i, new_j = i, j+1

    if new_j >= 0 and new_j < 3:
        new_puzz_state = state.copy()
        new_puzz_state[i,j] = state[new_i,new_j]
        new_puzz_state[new_i, new_j] = 0
        pos_zero = (i,j)
        return new_puzz_state
    return False

node_book = dict()
unique_node_key = 1
#Creating nodes from current state when tile is moved
def create_node(current_state, parent_key, cost2come = 0):

    global unique_node_key
    for key, node in node_book.items():
        if np.array_equal(current_state, node.state):
            return node

    node = Node(current_state, unique_node_key, parent_key, cost2come)
    node_book[unique_node_key] = node
    unique_node_key += 1

    

    return node
#Getting the node key of state from key
def get_node_key(state):

    for key, node in node_book.items():
        if np.array_equal(state, node.state):
            return key
    
    return False

#getting key of the node from the dict when node value is given
def get_node_from_key(node_key):
    global node_book
    for key, node in node_book.items():
        if node_key == key:
            return node
    return False
#fetching nodes from the state
def get_node_from_state(node_state):
    global node_book
    for key, node in node_book.items():
        if np.array_equal(node_state, node.state):
            return node
    return False

#checking if the current node is already visited
def already_visited(current_state, visited_queue):

  for state in visited_queue:
    if np.array_equal(state, current_state):
       return True

  return False

#getting child nodes after moving the tile
def get_child_nodes(current_state):

    possible_states = []

    if type(move_up(current_state)) != bool:
        possible_states.append(move_up(current_state))

    if type(move_down(current_state)) != bool:
        possible_states.append(move_down(current_state))

    if type(move_right(current_state)) != bool:
        possible_states.append(move_right(current_state))

    if type(move_left(current_state)) != bool:
        possible_states.append(move_left(current_state))

    return possible_states

#breadth first search function
def bfs(start_matrix, goal_matrix):

    curr_node = create_node(start_matrix, 0, 0)

    open_queue = []
    open_queue.append(curr_node.node_key) 

    visited_queue = [] # record visited states

    while len(open_queue):
        current_node = get_node_from_key(open_queue.pop(0))
        visited_queue.append(current_node.node_key)

        if np.array_equal(goal_matrix, current_node.state):
            print("yep! that's the goal.")
            break


        # next_states = subnodes(current_node_key)
        next_states = get_child_nodes(current_node.state)

        for state in next_states:
            if not already_visited(state, visited_queue):
                new_cost = current_node.cost2come + 10
                new_node = create_node(state, current_node.node_key, new_cost)
                open_queue.append(new_node.node_key)


        
    print(len(visited_queue))
    return plan_path(), visited_queue

#planning the after the search
def plan_path():

    path = []              
    path.append(goal_matrix)

    current_node = get_node_from_state(goal_matrix)

    while True:
        current_node = get_node_from_key(current_node.parent_key)

        path.append(current_node.state)

        if np.array_equal(start_matrix, current_node.state):
            break
    
    return path[::-1]

#writting the output file
def file_writer(path_states, visited_states):

        with open("nodePath.txt", 'w') as file:
            for state in path_states:
                file.write("\n")
                for val_array in list(state.T):                    
                    for val in val_array:                        
                        file.write(str(val)+ " ")

        with open("Nodes.txt", 'w') as file:
            for state in [get_node_from_key(node_key).state.T for node_key in visited_states]:
                file.write("\n")
                for val_array in list(state):
                    
                    for val in val_array:                        
                        file.write(str(val)+ " ")

        with open("NodesInfo.txt", 'w') as file:
            for node in [get_node_from_key(node_key) for node_key in visited_states]:
                file.write("\n")
                try :                                       
                    file.write(str(node.node_key)+ " "+ str(node.parent_key)+ " "+ str(node.cost2come)+ " ")
                except:
                    pass


if __name__ == "__main__":

    # taking user input for start matrix
    print("Please enter the start matrix (a11 a12 a13 a21 a22 a23 a31 a32 a33):  ", end="")
    start_input = input().split(" ")
    start_matrix = []
    for val in start_input:
        start_matrix.append(int(val))

    print("Please enter the goal puzzle matrix (a11 a12 a13 a21 a22 a23 a31 a32 a33):  ", end="")
    goal_input = input().split(" ")
    goal_matrix = []
    for val in goal_input:
        goal_matrix.append(int(val))

    start_matrix = np.array([start_matrix]).reshape((3,3))
    goal_matrix = np.array([goal_matrix]).reshape((3,3))

    # start_matrix = np.array([[4, 7, 0], [1, 2, 8], [3, 5, 6]])
    # goal_matrix = np.array([[1, 4, 7], [2, 5, 8], [3, 6, 0]])

    planned_path, visited_queue = bfs(start_matrix, goal_matrix)
    print(visited_queue)
    file_writer(planned_path, visited_queue)
    
