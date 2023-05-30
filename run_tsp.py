import pygad
import numpy as np
import matplotlib.pyplot as plt
import cec2017.functions as cec
import statistics as st
import random

class City():
       """     leCipares(): minera o arquivo retorna a array de cipares 
               fitness(individuo): calcula e retorna a FOB, que é a distancia 
       """
       def __init__(self):
              self.cty = self.leCidades()

       def fitness(self, ga_inst , indv , solut_idx): 
              sum = 0
              LEN = len(indv)
              for i in range(LEN):
                     j = indv[i] - 1
                     if i < LEN -1:
                            k = indv[i+1] -1
                     else: 
                            k = indv[0] -1
                     sum += np.sqrt((self.cty[j,1]-self.cty[k,1])**2+(self.cty[j,2]-self.cty[k,2])**2)
              return 1/(sum+0.000000001)
       
       def leCidades(self):
              list_line = []
              f = open('berlin52.tsp','r')
              for i in f:
                     list_line.append(i)
              f.close()
              #convertendo o arquivo (agora, lista) para matriz de inteiros com cidades na forma A= [cityNumber, X, Y]

              for i in range(len(list_line)):
                     list_line[i] =  list_line[i].rstrip().split()
              del list_line[-1]
              for i in range(len(list_line)):
                     for j in range(3):
                            list_line[i][j] = int(float(list_line[i][j]))
              return np.array(list_line)
       
       def CX_crossover (self, parents, offspring_size, ga_instance):
              offspring = []
              idx = 0
              while len(offspring) != offspring_size[0]:
                     parent1 = parents[idx % parents.shape[0], :].copy()
                     parent2 = parents[(idx + 1) % parents.shape[0], :].copy()
                     fit1 = self.fitness(None, parent1,None)
                     fit2 = self.fitness(None, parent2,None)
                     if (fit1 > fit2):
                            random_split_point = np.random.choice(range(int(offspring_size[1]/2)))
                            son_n = parent1[random_split_point:]
                            for city in parent2:
                                   if not city in son_n:
                                          son_n = np.concatenate((son_n,[city]))
                     else:
                            random_split_point = np.random.choice(range(int(offspring_size[1]/2)))
                            son_n = parent2[random_split_point:]
                            for city in parent1:
                                   if not city in son_n:
                                          son_n = np.concatenate((son_n,[city]))
              
                     offspring.append(son_n)
                     idx += 1
              return np.array(offspring)
       
       def mutation_func(self, offspring, ga_instance):
              for indv in range(offspring.shape[0]):
                     leng = offspring.shape[1]
                     random_split_point1 = np.random.choice(range(int(leng/2)))
                     random_split_point2 = np.random.choice(range(int((leng)/2),leng))
                     offspring[random_split_point1:random_split_point2+1]=offspring[random_split_point1:random_split_point2+1][::-1]   

              return offspring
'''
''
'      INICIALIZACAO E INSTANCIA DO G.A
''
'''
if __name__ == '__main__':
       np.set_printoptions(threshold=np.inf)
       gene_space={'low': 1, 'high': 130}
       init_range_low = 1
       init_range_high = 130
       num_generations = 1200
       sols = 60
       populacao = np.zeros((sols,init_range_high),dtype= int)
       for i in range(sols):
              populacao[i] = np.random.permutation(init_range_high)+1
       num_parents_mating =  int(sols*0.3)
       mutation_probability = 0.4
       parent_selection_type = "sss" 
       keep_parents = int(num_parents_mating*0.5)
       keep_elitism = 4
       city = City()   
       ga_instance = pygad.GA( num_generations = num_generations,
                                   num_parents_mating = num_parents_mating,
                                   # mutation_type = "swap",
                                   crossover_type= city.CX_crossover,
                                   # mutation_num_genes= 10,
                                   mutation_type = city.mutation_func,
                                   mutation_probability = mutation_probability,
                                   parent_selection_type = parent_selection_type,
                                   allow_duplicate_genes= False,
                                   keep_parents = keep_parents,
                                   fitness_func = city.fitness,
                                   gene_space = gene_space,
                                   gene_type = int,
                                   initial_population = populacao)
       # Execução do algoritmo genético
       ga_instance.run()
       ga_instance.plot_fitness()
       solution, solution_fitness, solution_i = ga_instance.best_solution()
       print(f"A melhor solucao foi a: {solution}, com aptidão: {solution_fitness}")
