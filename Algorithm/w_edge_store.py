import math
import random
import numpy as np

class w_edgestore:

    def __init__(self, s_e, s_w):

        self._max_edge_res_size = s_e
        self._max_wedge_res_size = s_w

        self._store = {} # adjacency list
        self._num_edges = 0
        self._debug = True
        self._edge_res = [None] * s_e

        self._wedge_res = [None]*s_w
        self._isClosed = [False]*s_w
    
    #Step 1 in UPDATE
    def markWedgesClosed(self, edge):
        u = edge[0]
        v = edge[1]

        for i in range(self._max_wedge_res_size):
            if self._wedge_res[i] == None:
                continue;
            wedge = self._wedge_res[i];

            if edge == wedge or edge == tuple(reversed(wedge)):
                #The edge closes the current wedge
                self._isClosed[i] = True
    
    #Step 3 in UPDATE
    def add(self,u,v):

        i = self._num_edges

        if self._num_edges >= self._max_edge_res_size:
            i = random.randint(0, self._num_edges-1)
            edge = self._edge_res[i]
            a = edge[0]
            b = edge[1]
            self._store[a].remove(b)
            self._store[b].remove(a)
            self._num_edges = self._num_edges - 1

        if u in self._store.keys():
            self._store[u].add(v)
        else :
            self._store[u]= set([v])

        if v in self._store.keys():
            self._store[v].add(u)
        else :
            self._store[v] = set([u])
        self._num_edges+=1

        self._edge_res[i] = (u, v)

    # Step 4 in UPDATE : To Calculate N_t
    def getNewWedges(self, u, v):
        wedges = []

        if u in self._store.keys():
            neighbors_u = self._store[u]
            for x in neighbors_u:
                wedges.append((x, v))

        if v in self._store.keys():
            neighbors_v = self._store[v]
            for x in neighbors_v:
                wedges.append((x, u))
        return wedges;
        
    #Steps 7-11 in UPDATE
    def updateWedges(self, new_wedges, heads_prob):
        num_changes = heads_prob * self._max_wedge_res_size;

        if num_changes <= 1:
            coin_toss = self.flip_coin(num_changes)
            if coin_toss == False:
                return
            old_wedge_index = random.randint(0, self._max_wedge_res_size-1)
            new_wedge_index = random.randint(0, len(new_wedges)-1)
            self._wedge_res[old_wedge_index] = new_wedges[new_wedge_index]
            self._isClosed[old_wedge_index] = False
            return

        old_wedges_index = random.sample(xrange(self._max_wedge_res_size), int(math.floor(num_changes)))

        for i in old_wedges_index:
            new_wedge_index = random.randint(0, len(new_wedges) - 1)
            self._wedge_res[i] = new_wedges[new_wedge_index]
            self._isClosed[i] = False

    #For Step 8 in UPDATE
    def flip_coin(self, head_prob):
        coin_toss = random.random()
        if coin_toss < head_prob :
            # print "Head"
            return True
        else:
            # print "Tail"
            return False

    #Step 3 in ALGORITHM
    def getWedgesClosedFraction(self):
        count_closed = 0
        for i in range(self._max_wedge_res_size):
            if self._isClosed[i] == True:
                count_closed = count_closed + 1
        num_wedges = self.getNumWedges()
        if num_wedges == 0:
            return 0
        return float(count_closed)/num_wedges;
            
    #Helper Method
    def getNumWedges(self):
        num_wedges = 0
        for i in range(self._max_wedge_res_size):
            if self._wedge_res[i] != None:
                num_wedges += 1
        return num_wedges

    def getWedges(self):
        total_wedges = []
        for i in range(self._num_edges-1):
            edge = self._edge_res[i]
            a = edge[0]
            b = edge[1]
            total_wedges.extend(self.getNewWedges(a, b));
        return total_wedges

    def printContents(self):
        print self._store

    def get_neighbours(self,u):
        return self._store[u]

    def get_num_edges(self):
        return self._num_edges

    def get_num_vertices(self):
        return len(self._store)

    def get_vertice_list(self):
        return self._store.keys()

    def get_edges(self):
        return list(self._edge_res)

def testEdgeStore(datafile):
    edge_store = w_edgestore()
    f = open(datafile)
    for line in f:
        op,u,v = line.split()
        if op == '+':
            edge_store.add(u,v)
        elif op == "-":
            edge_store.delete(u,v)
    #print edge_store._store
    edge_store.printContents()
    print "neighbours of 3:"
    print edge_store.get_neighbours('3')
    edge_store.add(4,5)
    edge_store.printContents()
    edge_store.delete(4,5)
    edge_store.printContents()


if __name__ == '__main__':
    datafile = "data/dummy.txt"
    testEdgeStore(datafile)

