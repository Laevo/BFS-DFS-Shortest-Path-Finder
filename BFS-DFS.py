#References
#For making Queue- http://code.activestate.com/recipes/210459-quick-and-easy-fifo-queue-class/
#For bfs concept- http://interactivepython.org/runestone/static/pythonds/Graphs/ImplementingBreadthFirstSearch.html
#                 and http://code.activestate.com/recipes/576675-bfs-breadth-first-search-graph-traversal/


# A Class for Nodes
class NodeClass:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost


# Fifo Queue for BFS
class FifoQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack =[]

    def push(self,val):
        self.in_stack.append(val)

    def pop(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack.pop()

    def empty_check(self):
        check = False
        if len(self.in_stack) == 0:
            check = True
        return check


# Open file and store as objects of the class into adjacency list
with open('input','r') as f:
    data = f.read()
    data = data.split('\n')
    city_list = {}
    for line in data:
        children = []
        line = line.split(',')
        parent = line[0]
        child = line[1]
        cost = line[2]
        node1 = NodeClass(child, parent, 'Travel', cost)    # Storing Arad-Zerind and also Zerind-Arad for reverse traversal
        node2 = NodeClass(parent, child, 'Travel', cost)
        if parent in city_list:
            children = city_list[parent]
            children.append(node1)
            city_list[parent] = children
        else:
            city_list[parent] = [node1]
        if child in city_list:
            children = city_list[child]
            children.append(node2)
            city_list[child] = children
        else:
            city_list[child] = [node2]



def initializeFrontier(start):  # Initializing stack and queue for searches
    queue = FifoQueue()
    queue.push([start])
    stack = [(start, [start])]
    return queue, stack


def chooseBfsNode(queue):
    path = queue.pop()
    node = path[len(path)-1]
    return node, path


def chooseDfsNode(stack):
    (node, path) = stack.pop()
    return node, path


def testGoal(node, end, path):
    cost = 0
    if node == end:     # Testing goal and calculating costs
        i = 0
        for k in range (1, len(path)):
            try:
                for child in city_list[path[i]]:
                    if child.state == path[i+1]:
                        cost = cost + int(child.path_cost)
                        i += 1
            except: continue
        return 'Yes', cost
    return 'No', cost

def expandNode_UpdateFrontier(graph, node, path, queue):
    if node in graph:
        for node in graph[node]:   #Expand Node
            if node.state not in path:
                new_path = path + [node.state]
                queue.push(new_path)    #Update Frontier
    else:
        previous_node = path[len(path)-2]   #Going to other children of previous node on a dead end
        for curr_node in graph[previous_node]:      #Expand Node
            if curr_node.state != node:
                if curr_node.state not in path:
                    new_path = path + [curr_node.state]
                    queue.push(new_path)    #Update Frontier



def bfs(graph,end, queue):
    while queue.empty_check() == False:
        node, path = chooseBfsNode(queue)
        result, cost = testGoal(node, end, path)
        if result == 'Yes':
            print "BFS Path : ",path
            print 'Cost : ', cost
            break
        expandNode_UpdateFrontier(graph, node, path, queue)


def dfs(graph, end, stack):
    while stack:
        node, path = chooseDfsNode(stack)
        if node in graph:
            for child in graph[node]:
                if child.state not in path:
                    result, cost = testGoal(child.state, end, path + [child.state])
                    if result == "Yes":
                        print "DFS Path : ", path + [child.state]
                        print "Cost : ", cost
                        return
                    stack.append((child.state, path + [child.state]))



def graphSearch(graph, start, end, strategy):
    queue, stack = initializeFrontier(start)
    if strategy == '1':
        bfs(graph, end, queue)
    elif strategy == '2':
        dfs(graph, end, stack)


start = raw_input('Enter source: ')
end = raw_input('Enter destination: ')
strategy = raw_input('Enter Search Strategy - '
                      '\n1 for BFS'
                      '\n2 for DFS'
                      '\n: ')
graphSearch(city_list, start, end, strategy)
