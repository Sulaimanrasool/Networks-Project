import numpy as np
import random as rand
import time


def conect_node(new_node, nestlist, all_n, m, p, q, edges, conection_list):
    """

    :param new_node: The new node that we want to connect
    :param nestlist: The adjacency nestlist
    :return: Updated adjacency nestlist , edges and degree dist

    This is the function to calculate and perform the connections between a new node and an old one
    """
    size = len(nestlist)
    prob_matrix = np.zeros([size - 1, 1])
    total = 0
    attach_type = [1, 2]
    conec_lenght = len(conection_list)
    found = []
    if p == 1:  # for preferential attachment
        m_check = []
        for i in range(m):
            ind = rand.randint(0,conec_lenght - 1)
            pot = conection_list[ind]
            while pot in m_check:
                ind = rand.randint(0, conec_lenght - 1)
                pot = conection_list[ind]
            found.append(pot)
            m_check.append(pot)

    if p == 2: # for random attachment
        m_check = []
        for i in range(m):
            ind = rand.randint(0, len(nestlist) - 2)
            while ind in m_check:
                ind = rand.randint(0, len(nestlist) - 2)
            found.append(ind)
            m_check.append(ind)

    if p == 3: # mixed attachement
        m_check = []
        for i in range(m):
            if q == 2/3 :
                probs = [0,0,1]
            elif q == 1/2:
                probs = [0,1]
            conec = probs[rand.randint(0,len(probs) - 1)]
            if conec == 0:
                ind = rand.randint(0, conec_lenght - 1)
                pot = conection_list[ind]
                while pot in m_check:
                    ind = rand.randint(0, conec_lenght - 1)
                    pot = conection_list[ind]
                found.append(pot)
                m_check.append(pot)
            else:
                ind = rand.randint(0, len(nestlist) - 2)
                while ind in m_check:
                    ind = rand.randint(0, len(nestlist) - 2)
                found.append(ind)
                m_check.append(ind)

    for j in found:
        if new_node not in nestlist[j]:
            nestlist[new_node].append(j)
            nestlist[new_node].sort()
            nestlist[j].append(new_node)
            nestlist[j].sort()
            conection_list.append(j)
            conection_list.append(new_node)
    edges.append(edges[-1] + m)

    return nestlist, edges, conection_list

def ba_model(n,m, p,q):
    """

    :param n: The number of nodes you want in the system
    :param m: The number of new edges per added node
    :param p: The type of attachment, p = 1 : preferential, p = 2 : random, p = 3: mixed
    :param q: The probability for p = 3. q is the probaiblity of picking preferential, and 1-q for random
    :return adjacency_matrix: Return the adjacency nestlist
    :return degree_dist: Return the degree dist
    :return adjaceny_list: Return the adajcnecy list
    :return edgess: Return the edges list
    """
    all_n = np.linspace(0,n-1,n)
    degree_dist = []
    connection_list = []
    adjacency_list = []
    for i in range(m+1):
        if i == 0:
            adjacency_list.append([])
        else:
            adjacency_list.append([])
            for j in range(i):
                 if i !=j :
                    adjacency_list[i].append(j)
                    adjacency_list[j].append(i)
                    connection_list.append(i)
                    connection_list.append(j)
    ini_size = len(adjacency_list)  # size of the initial  nestlist

    edges = [1, 2, 3]
    for i in range(ini_size,n):   # new nodes not counting the initial simple graph nodes
        adjacency_list.append([])
        adjacency_list, edges, connection_list = conect_node(i,adjacency_list, all_n, m, p, q, edges, connection_list)

    for ele in adjacency_list:
        degree_dist.append(len(ele))

    return adjacency_list, degree_dist, edges


def main():
    start = time.time()
    ad, deg, edges = ba_model(1000, 4, 3, 2/3)
    print(len(deg))
    print(ad)
    print(deg)
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()