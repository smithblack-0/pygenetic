import sys 
sys.path.append('../../pyGenetic/')

import GAEngine, ChromosomeFactory, Utils
import matplotlib.pyplot as plt

def fitness(board):
		fitness = 0
		for i in range(len(board)):
			isSafe = True
			for j in range(len(board)):
				if i!=j:
					if (board[i] == board[j]) or (abs(board[i] - board[j]) == abs(i-j)):
						isSafe = False
						break
			if(isSafe==True):
				fitness += 1
		return fitness

factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=4,minValue=1,maxValue=4)
ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)

ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
ga.addMutationHandler(Utils.MutationHandlers.swap)

ga.setSelectionHandler(Utils.SelectionHandlers.basic)
ga.setFitnessHandler(fitness)

ga.evolve(3)

#fig = ga.statistics.plot_statistics(['best','worst','avg'])
#plt.show()
#fig = ga.statistics.plot_statistics(['diversity','mutation_rate'])
#plt.show()