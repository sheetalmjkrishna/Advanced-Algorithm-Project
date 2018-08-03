from __future__ import division
from w_edge_store import w_edgestore
import random
from datetime import datetime

class algorithm:

    # setup
    def __init__(self,s_e, s_w):
        self._s_e = s_e
        self._s_w = s_w
        self.w_edge_store = w_edgestore(s_e, s_w)
        self._debug = True

    # Simulates flipping a coin
    # Params: head_prob : probability of Heads
    # Returns: if Heads return True else return False
    def flip_coin(self,head_prob):
        coin_toss = random.random()
        if coin_toss < head_prob :
            # print "Head"
            return True
        else:
            # print "Tail"
            return False

    # implemts reservoir sampling
    # Returns: if edge can be added to sample edgeset:S  else false
    def sample_edge(self, t):
        if t <= self._s_e:
            return True

        else:
            # print "No space for edge (%s,%s)" % (edge[0], edge[1])
            heads_prob = 1 - ((1 - float(1)/t)**self._s_e)
            coin_toss = self.flip_coin(heads_prob)
            return coin_toss

    def run(self, datafile):
        t = 0
        f = open(datafile)

        lines = f.readlines()
        #random.shuffle(lines)

        for line in lines:

            #if t!=0 and t%499==0:
                #print('At ' + str(t))

            input = line.split()
            u = input[0]
            v = input[1]
            if u==v :
                continue
            if u > v:
                tmp = u
                u = v
                v = tmp
            if (u,v) in self.w_edge_store.get_edges():
                continue

            t=t+1

            self.w_edge_store.markWedgesClosed((u, v))

            if self.sample_edge(t):
                self.w_edge_store.add(u, v)

                N_t = self.w_edge_store.getNewWedges(u, v)
                new_wedges_size = len(N_t)

                total_wedges = self.w_edge_store.getWedges()
                total_wedges_size = len(total_wedges)

                if total_wedges_size == 0:
                    q = 0
                else:
                    q = float(new_wedges_size)/total_wedges_size

                self.w_edge_store.updateWedges(total_wedges, q)

            rho = self.w_edge_store.getWedgesClosedFraction()
            kappa_t = 3*rho

            triangle_count_t = rho * t * t
            triangle_count_t = triangle_count_t/self._s_e
            triangle_count_t = triangle_count_t / (self._s_e - 1)
            triangle_count_t = triangle_count_t * total_wedges_size

            if t%2000 == 0 or t==len(lines) - 1 :
                print(str(datetime.now()) + ' : t = ' + str(t) + ', Kappa_t = ' + str(kappa_t) + ', Traingle Count at t : '+str(triangle_count_t))


def test_file(datafile):
    f = open(datafile)
    for line in f:
        u, v, weight = line.split()
        print "%s,%s"%(u,v)


if __name__ == '__main__':
    random.seed(1234)

    #M=100 for data/facebook_combined.txt, count_triangles = 1730053, transitivity = 0.03

    datafile = "data/facebook_combined.txt"
    s_e = 100
    s_w = 100
    
    obj = algorithm(s_e, s_w)
    count = obj.run(datafile)
