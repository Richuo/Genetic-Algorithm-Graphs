from graphviz import Digraph
import pandas as pd
import random

G = Digraph(format='pdf')

G.attr(rankdir='LR', size='8,5')
G.attr('node', shape='circle')

min_random,max_random = 1, 100
size_graph = 30
number_of_moves = (size_graph-1)*2 


#Create graph
src_list = []
dst_list = []
weight_list = []

for x in range(size_graph):
    for y in range(size_graph):
        if x != size_graph-1 and y != size_graph-1:
            rand_number = random.randint(min_random,max_random)
            src_list.append('%s,%s' % (x,y))
            dst_list.append('%s,%s' % (x+1,y))
            weight_list.append(rand_number)
            rand_number = random.randint(min_random,max_random)
            src_list.append('%s,%s' % (x,y))
            dst_list.append('%s,%s' % (x,y+1))
            weight_list.append(rand_number)
        elif x == size_graph-1 and y != size_graph-1:
            rand_number = random.randint(min_random,max_random)
            src_list.append('%s,%s' % (x,y))
            dst_list.append('%s,%s' % (x,y+1))
            weight_list.append(rand_number)
        elif x != size_graph-1 and y == size_graph-1:
            rand_number = random.randint(min_random,max_random)
            src_list.append('%s,%s' % (x,y))
            dst_list.append('%s,%s' % (x+1,y))
            weight_list.append(rand_number)

print(src_list,dst_list,weight_list)

d = {'src': src_list, 'dst': dst_list, 'weight': weight_list}

df = pd.DataFrame(data=d)

nodelist = []
for idx, row in df.iterrows():
    node1, node2, weight = [str(i) for i in row]

    if node1 not in nodelist:
        G.node(node1)
        nodelist.append(node2)
    if node2 not in nodelist:
        G.node(node2)
        nodelist.append(node2)

    G.edge(node1,node2, label = weight)

G.render('sg', view=True)

df.to_csv('data_graph.csv', encoding='utf-8',index=False)

