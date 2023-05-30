import pygad
import numpy as np
import matplotlib.pyplot as plt
import cec2017.functions as cec
import statistics as st

def func(X):
    return cec.f4([X])[0]
# Inicialização dos termos
D = 10
N = 51
orcamento = 10000*D
sol_per_exec = int(orcamento/N)
init_range_low = -2
init_range_high = 2
pop_size = (sol_per_exec, D)

# Execução das 51 otimizações independentes
best_solutions = []
best_fitness = []
for i in range(N):
    # Criação da população inicial 
    populacao =  np.random.uniform(low=init_range_low, high=init_range_high, size=pop_size)
    #Função de aptidão 
    # def mutation_func(offspring, ga_instance):
    #     for chromosome_idx in range(offspring.shape[0]):
    #         random_gene_idx = np.random.choice(range(offspring.shape[1]))
    #         offspring[chromosome_idx, random_gene_idx] += np.random.random()
    #     return offspring
    def fitness_func(ga_instance, solution, solution_idx):
        fitness = 1.0 / (func(solution) + 0.0000000001)
        return fitness
    # Criação do algoritmo genético
    num_generations = int(orcamento / (sol_per_exec * D))
    num_parents_mating = int(0.5*sol_per_exec)
    mutation_probability = [0.7,0.1] #0.3 
    parent_selection_type = "sss" 
    keep_parents = int(sol_per_exec/7)   
    keep_elitism = int(sol_per_exec*0.2)     
    ga_instance = pygad.GA( num_generations = num_generations,
                            num_parents_mating = num_parents_mating,
                            mutation_type = "adaptive",
                            #    mutation_type = mutation_func,
                            mutation_probability = mutation_probability,
                            parent_selection_type = parent_selection_type,
                            keep_parents = keep_parents,
                            fitness_func = fitness_func,
                            gene_space = {'low': -100, 'high': 100},
                            initial_population = populacao)
    # Execução do algoritmo genético
    ga_instance.run()
    # Salva a melhor solução da execução atual
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    best_solutions.append(solution)
    best_fitness.append(func(solution))

plt.plot(best_solutions)
plt.title('Fitness ao longo das gerações')
plt.xlabel('Gerações')
plt.ylabel('Fitness')
plt.show()
print(best_fitness)
print("Best: {} ".format(min(best_fitness)))
print("Worst: {} ".format(max(best_fitness)))
print("Std: {}".format(st.stdev(best_fitness)))
print("Mediana: {}".format(st.median((best_fitness))))
