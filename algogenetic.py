from graphviz import Digraph
import pandas as pd
import random
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import numpy as np
from colorama import Fore, Back, Style


number_of_people = 50 #input
number_of_generations = 500
elite_size = 10
mutation_rate = 0.01
size_graph = 30
number_of_moves = (size_graph-1)*2 

total_score = []
total_score_average = []

df = pd.read_csv('data_graph.csv', sep=",", engine='python')
dict_df = df.to_dict()
src_list = list(dict_df['src'].values())
dst_list = list(dict_df['dst'].values())
weight_list = list(dict_df['weight'].values())

def initialisation():
    series = [] #0 go down, 1 go right
    nb_0 = 0
    nb_1 = 0
    for i in range(number_of_moves):
        if nb_1 == number_of_moves/2:
            series.append(0)
        elif nb_0 == number_of_moves/2:
            series.append(1)
        else:
            chosen_number = random.randint(0, 1)
            if chosen_number == 0:
                nb_0 += 1
            else:
                nb_1 += 1
            series.append(chosen_number)
    return(series)


def move(series):
    score = 0
    series_loc = series[:]
    x,y = 0,0
    for i in range(number_of_moves):
        coord_src = ('%s,%s' %(x,y))
        if series_loc[0] == 0:
            y += 1
        else:
            x += 1
        coord_dst = ('%s,%s' %(x,y))
        series_loc.pop(0)
        df_weight = weight_list[[i for i, e in enumerate(dst_list) if e == coord_dst and src_list[i] == coord_src][0]]
        #df.loc[np.logical_and.reduce((df['dst'] == coord_dst, df['src'] == coord_src))]['weight'].tolist()[0] #loc[(df['dst'] == coord_dst) & (df['src'] == coord_src)]['weight'].tolist()[0]
        score += df_weight
    return(score)


def firstGeneration():
    dict_score_series = {}
    score_list = []
    pop_list = []
    for i in range(number_of_people):
        series = initialisation()
        score = move(series)
        score_list.append(score)
        dict_score_series[score] = series
        pop_list.append(series)
    return(score_list, dict_score_series, pop_list)


def elitism(score_list, dict_score_series, pop_list, elitesize):
    new_pop = []
    score_pop_list = []
    total_pop_nb = len(score_list)
    sorted_score_list = sorted(score_list)

    for i in range(elitesize):
        score_pop = sorted_score_list.pop(0)
        elite_pop = dict_score_series[score_pop]
        new_pop.append(elite_pop)
        score_pop_list.append(score_pop)

    for i in range(total_pop_nb - elitesize):
        score_pop = random.choice(sorted_score_list)
        pop_loc = dict_score_series[score_pop]
        new_pop.append(pop_loc)
        score_pop_list.append(score_pop)

    return(new_pop, score_pop_list)


def breed(parent1, parent2): #Uniform crossing
    child1 = []
    child2 = []

    length_gene = len(parent1)
    nb_0 = 0
    nb_1 = 0
    for i in range(length_gene):
        rand_choice = random.random()
        if rand_choice < 0.5 and nb_0 < length_gene/2 :
            child1.append(0)
            child2.append(1)
            nb_0 += 1
        elif rand_choice >= 0.5 and nb_1 < length_gene/2 :
            child1.append(1)
            child2.append(0)
            nb_1 += 1
        elif nb_0 >= length_gene/2:
            child1.append(1)
            child2.append(0)
        elif nb_1 >= length_gene/2:
            child1.append(0)
            child2.append(1)

    return(child1, child2)


def breeding(new_pop,elitesize):
    children = []
    total_pop_nb = len(new_pop)
    random_pop = random.sample(new_pop, len(new_pop))

    for i in range(elitesize):
        children.append(new_pop[i])

    for i in range(int((total_pop_nb - elitesize)/2)):
        parent1,parent2 = random_pop.pop(0),random_pop.pop(0)
        child1, child2 = breed(parent1,parent2)
        children.append(child1)
        children.append(child2)

    return(children)


def mutation(children, mutationrate, elitesize):
    for i in range(elitesize, len(children)):
        pop = children[i]
        for index_gene in range(len(pop)):
            if random.random() < mutationrate:
                random_gene = int(random.random()*len(pop))
                gene_mutate, gene_modified = pop[random_gene], pop[index_gene]
                pop[index_gene], pop[random_gene] = gene_mutate, gene_modified

    return(children)


def nextGeneration(score_list, dict_score_series, pop_list, elitesize, mutationrate):
    #print('PARENTS : ', pop_list)
    #print('SCORE PARENTS : ', score_list)
    new_pop, new_score_pop_list,  = elitism(score_list, dict_score_series, pop_list, elitesize)
    children = breeding(new_pop, elitesize)
    #print('CHILDREN : ', children)
    nextGeneration = mutation(children, mutationrate, elitesize)
    #print('MUTATED CHILDREN : ', nextGeneration)
    new_score_list, new_dict_score_pop = evaluate(nextGeneration)
    return(new_score_list, new_dict_score_pop, nextGeneration)

def evaluate(new_generation):
    new_dict_score_pop = {}
    new_score_list = []
    for pop in new_generation:
        score = move(pop)
        new_score_list.append(score)
        new_dict_score_pop[score] = pop

    #print("Score list : ", new_score_list)
    min_score = min(new_score_list)
    min_pop = new_dict_score_pop[min_score]
    total_score.append(min_score)
    average_list = sum(new_score_list)/len(new_score_list)
    total_score_average.append(average_list)
    #print('The fastest way is : %s' % min_score)
    #print('Its series is : %s' % min_pop)
    return(new_score_list, new_dict_score_pop)

def fitness():
    score_fitness = 0



print("SUMMARY")
print("Size of the graph : %s \nSize of the population : %s \nNumber of generations : %s \nElite size : %s \nMutation rate : %s" % (size_graph, number_of_people, number_of_generations, elite_size, mutation_rate))

print("\nRunning the program...")
start_time = time.time()

score_list, dict_score_series, pop_list = firstGeneration()

end_time1 = time.time()
timer = end_time1 - start_time
approx_time = timer * number_of_generations
print("It will take approximately %s seconds (%s minutes)" % (str(round(approx_time, 2)), str(round(approx_time/60, 1))))

#print("First population score : ", sorted(score_list))
average_list = sum(score_list)/len(score_list)
print("Average Score of the first population : ", average_list)

pbar = tqdm([i for i in range(number_of_generations)])


for i in range(number_of_generations):
    score_list, dict_score_series_plus, pop_list = nextGeneration(score_list, dict_score_series, pop_list, elite_size, mutation_rate)
    dict_score_series.update(dict_score_series_plus)
    pbar.update()
    pbar.set_description("Processing generation %s" % str(i+1))

print("Program done")

end_time2 = time.time()
timer = end_time2 - start_time
print("It has taken %s seconds" % str(round(timer, 2)))

#print("Last population score : ", sorted(score_list))
average_list = sum(score_list)/len(score_list)
print("Average Score of the last population: ", average_list)

#print("SCORE AVERAGE : ", total_score_average)
#print("TOTAL SCORE : ", total_score)
try :
    best_score = min(total_score)
    print("Fastest found : " + '\033[92m' + str(best_score))
    print(Style.RESET_ALL)
    print("Best pop is : ", dict_score_series[best_score])
except:
    print("Error with the dictionary")
    pass;


plt.plot(total_score, 'r', label='Best score of a generation')
#plt.plot(total_score_average, 'g', label='Average score of a generation')
plt.ylabel('Distance')
plt.xlabel('Generation')
plt.legend()
plt.savefig('graph_score.png')
plt.show()
