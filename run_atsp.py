import pygad
import numpy as np
import matplotlib.pyplot as plt
import cec2017.functions as cec
import statistics as st
import random

class CityATSP():
       """     
       Esta classe lê os arquivos .tsp e .atsp e possui os operadores genéticos para problemas de TSP por algoritmo genético
       init: (len)-> required only at unalined ATSPS files 
       """
       def __init__(self, **kwargs):
            self.cty = self.ReadDists_TSP_lined()
            # self.len = 71
            print(self.cty)
       """
       Processa os arquivos .atsp e .tsp
       Return: dicionário{n-1 city: np.array([dist0, dist1, ...,distn])}
       """
       def ReadDists_TSP_lined(self):
            path = {}
            f = open('br17.atsp','r')
            for idx, line in enumerate(f, start=0):
                path[idx] = line 
            f.close()
            for i,line in path.items(): 
                path[i] =  line.rstrip().split()
            for line in path.values():
                for i in range(len(line)):
                      line[i] = int(line[i])
            del path[17]
            return path
       """
       Processa os arquivos .atsp e .tsp que ja nao estejam organizados no layout correto 
       Return: dicionário{n-1 city: np.array([dist0, dist1, ...,distn])}
       """
       def ReadDists_ATSP_unalined(self): 
            path = {}
            line = []
            f = open('ftv70.atsp','r')
            for i in f:
                line.append(i)
            f.close()
            for i in range(len(line)): 
                line[i] =  line[i].rstrip().split()
            for lin in line:
                for col in range(len(lin)):
                      lin[col] = int(lin[col])
            line =  [elemento for line in line for elemento in line]
            n_keys = len(line) // 71

            for i in range(n_keys):
                cut1 = i * 71
                cut2 = cut1 + 71
                route = line[cut1:cut2]
                path[i] = route

            return path
       """
       Função de aptidão para biblioteca PyGAD
       """
       def fitness(self, ga_inst ,indv , solut_idx): 
              sum = 0
              LEN = len(indv)
              for i in range(LEN):
                    j = indv[i] - 1
                    if i < LEN -1:
                        k = indv[i+1] -1
                    else: 
                        k = indv[0] -1
                        
                    sum += self.cty[j][k]
              return 1/(sum+0.000000001)
       """
       Cross-over personalizado sem repetição para PyGAD
       """
       def CX_crossover (self, parents, offspring_size, ga_instance):
              offspring = []
              idx = 0
              while len(offspring) != offspring_size[0]:
                     parent1 = parents[idx % parents.shape[0], :].copy()
                     parent2 = parents[(idx + 1) % parents.shape[0], :].copy()
                     fit1 = self.fitness(None, parent1,None)
                     fit2 = self.fitness(None, parent2,None)
                     if (fit1> fit2):
                            random_split_point = np.random.choice(range(int(offspring_size[1]*0.5)))
                            son_n = parent1[random_split_point:]
                            for city in parent2:
                                   if not city in son_n:
                                          son_n = np.concatenate((son_n,[city]))
                     else:
                            random_split_point = np.random.choice(range(int(offspring_size[1]*0.5)))
                            son_n = parent2[random_split_point:]
                            for city in parent1:
                                   if not city in son_n:
                                          son_n = np.concatenate((son_n,[city]))   
                     offspring.append(son_n)
                     idx += 1
              return np.array(offspring)
       """
       Mutação personalizada sem repetição para PyGAD
       """
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
       print("Personalize os defines aqui dependendo do .tsp")
       print("Problemas em dimensao D<50: sols=40 e D>50: sols=70")
       np.set_printoptions(threshold=np.inf)

       city = CityATSP()
       gene_space={'low': 1, 'high': 17}
       init_range_low = 1
       init_range_high = 17
       num_generations = 1200
       sols = 40
       populacao = np.zeros((sols,init_range_high),dtype= int)
       for i in range(sols):
              populacao[i] = np.random.permutation(init_range_high)+1
       num_parents_mating =  int(sols*0.3)
       mutation_probability = 0.4
       parent_selection_type = "tournament" 
       keep_parents = int(num_parents_mating*0.5)
       keep_elitism = 3
       city = CityATSP()
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
                                   initial_population = populacao,
                                   crossover_probability= 0)
       # Execução do algoritmo genético
       ga_instance.run()
       ga_instance.plot_fitness()
       solution, solution_fitness, solution_i = ga_instance.best_solution()
       print(f"A melhor solucao foi a: {solution}, com aptidão: {solution_fitness}")
    #    print(f"O erro realtivo foi {}%" )



