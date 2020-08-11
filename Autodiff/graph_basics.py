class GraphAdjList(object):

    def __init__(self, vertex_number):
        """create list of list"""
        self.vertex_number = vertex_number
        self.lists = [[i] for i in range(vertex_number)]

    def add_edge(self, i, j):
        self.lists[i].append(j)
        # self.lists[j].append(i)

    def print(self):
        for list in self.lists:
            print("->".join(map(str, list)))

    def bfs_traversal_queue(self, start):
        """BFS using queue"""
        visited = [False] * self.vertex_number

        # list = self.lists[start]
        queue = []
        queue.append(start)
        visited[start] = True

        while queue:
            s = queue.pop(0)
            """Processing the node"""
            print(s)
            """"""
            for i in self.lists[s]:
                if not visited[i]:
                    visited[i] = True
                    queue.append(i)
                    
    # FIXME: wrong solution with stack!
    def dfs_traversal_stack(self, start):
        """DFS using stack"""
        visited = [False] * self.vertex_number

        stack = []
        visited[start] = True
        stack.append(start)

        while stack:
            top = stack.pop()
            print(top)
            for i in self.lists[top]:
                if not visited[i]:
                    visited[i] = True
                    stack.append(i)

    def dfs_traversal_recursion(self, start):
        """DFS using recursion"""
        visited = [False] * self.vertex_number

        def dfs(current, visited):
            if not visited[current]:
                """Processing the node"""
                print(current)
                """"""
                visited[current] = True
                for i in self.lists[current]:
                    dfs(i, visited)

        dfs(start, visited)


def read_print(filename):
    with open(filename, 'r') as f:
        contents = f.readlines()

    nb_tests = int(contents[0])
    head_line_number = 1

    for i in range(nb_tests):
        nb_vertex, nb_edge = map(int, contents[head_line_number].split(' '))
        graph = GraphAdjList(nb_vertex)
        for j in range(head_line_number + 1, head_line_number + nb_edge + 1):
            graph.add_edge(*(map(int, contents[j].split(' '))))
        graph.print()
        head_line_number = head_line_number + nb_edge + 1


"""
Version for nodes in linkedlist 
"""


class Node(object):
    """Node in linked list"""

    def __init__(self, val: int):
        self.vertex = val
        # pointer to the next node
        self.next = None

    def point_to(self, node):
        self.next = node


class Graph(object):

    def __init__(self, number_vertex: int):
        self.n_vertex = number_vertex
        self.graph = [None] * self.n_vertex

    def add_edge(self, i, j):
        node = Node(j)
        node.point_to(self.graph[i])
        self.graph[i] = node

        node = Node(i)
        node.point_to(self.graph[j])
        self.graph[j] = node

    def print_graph(self):
        for i in range(self.n_vertex):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")


if __name__ == "__main__":
    # read_print('input')
    g = GraphAdjList(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 3)
    g.print()
    g.dfs_traversal_stack(1)
    g.dfs_traversal_recursion(1)

    # V = 5
    # graph = Graph(V)
    # graph.add_edge(0, 1)
    # graph.add_edge(0, 4)
    # graph.add_edge(1, 2)
    # graph.add_edge(1, 3)
    # graph.add_edge(1, 4)
    # graph.add_edge(2, 3)
    # graph.add_edge(3, 4)
    #
    # graph.print_graph()
