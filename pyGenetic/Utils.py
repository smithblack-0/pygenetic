import random
import copy
import math
import operator

class SelectionHandlers:
	"""
	Class contains staticmethods for selection operation which are
	invoked by  Evolution.py module during selection operation
	
	Methods :
	--------
	basic() : Performs selection operation based fitness scores of candidates

	"""

	@staticmethod
	def random(fitness_mappings, ga):
		pop = [x[0] for x in fitness_mappings]
		return [random.choice(pop) for i in range(len(fitness_mappings)-math.ceil(ga.cross_prob * len(fitness_mappings)))]

	@staticmethod
	def smallest(fitness_mappings, ga):
		new = sorted(fitness_mappings, key=operator.itemgetter(1))[:len(fitness_mappings)-math.ceil(ga.cross_prob * len(fitness_mappings))]
		return [i[0] for i in new]
		
	@staticmethod
	def largest(fitness_mappings, ga):
		new = sorted(fitness_mappings, key=operator.itemgetter(1), reverse=True)[:len(fitness_mappings)-math.ceil(ga.cross_prob * len(fitness_mappings))]
		return [i[0] for i in new]

	@staticmethod
	def best(fitness_mappings, ga):
		if ga.fitness_type == 'max':
			new = sorted(fitness_mappings, key=operator.itemgetter(1), reverse=True)[:len(fitness_mappings)-math.ceil(ga.cross_prob * len(fitness_mappings))]
		elif ga.fitness_type == 'min':
			new = sorted(fitness_mappings, key=operator.itemgetter(1))[:len(fitness_mappings)-math.ceil(ga.cross_prob * len(fitness_mappings))]
		elif ga.fitness_type[0] == 'equal':
			new = sorted(fitness_mappings, key=lambda x:abs(x[1]-ga.fitness_type[1]))[:len(fitness_mappings)-math.ceil(ga.cross_prob * len(fitness_mappings))]
		return [i[0] for i in new]
		
	@staticmethod
	def tournament(fitness_mappings, ga, tournsize):
		print("\n\n\ntournsize = ",tournsize,"\n\n\n")
		chosen = []
		for i in range(len(fitness_mappings)-math.ceil(ga.cross_prob * len(fitness_mappings))):
			aspirants = random.sample(fitness_mappings, tournsize)
			if ga.fitness_type == 'max':
				chosen.append(max(aspirants, key=operator.itemgetter(1)))
			elif ga.fitness_type == 'min':
				chosen.append(min(aspirants, key=operator.itemgetter(1)))
			elif ga.fitness_type[0] == 'equal':
				for x in range(tournsize):
					aspirants[x] = (aspirants[x][0],abs(aspirants[x][1] - ga.fitness_type[1]))
				chosen.append(min(aspirants, key=operator.itemgetter(1)))
		return [i[0] for i in chosen]
		
	@staticmethod
	def roulette(fitness_mappings, ga):
		fitness = [i[1] for i in fitness_mappings]
		if ga.selection_handler == SelectionHandlers.roulette:
			if ga.fitness_type == 'max':
				pass
			elif ga.fitness_type == 'min':
				maxim = max(fitness)
				fitness = [maxim-x for x in fitness]
			elif ga.fitness_type[0] == 'equal':
				fitness = [abs(x-ga.fitness_type[1]) for x in fitness]
				maxim = max(fitness)
				fitness = [maxim-x for x in fitness]
		total_fit = float(sum(fitness))
		relative_fitness = [f/total_fit for f in fitness]
		probabilities = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]
		chosen = []
		pop = [x[0] for x in fitness_mappings]
		print("\n\n\n",pop,"\n\n\n")
		print("\n\n\n",fitness,"\n\n\n")
		for n in range(len(fitness_mappings)-math.ceil(ga.cross_prob * len(fitness_mappings))):
			r = random.random()
			for (i, individual) in enumerate(pop):
				if r <= probabilities[i]:
					chosen.append(list(individual))
					break
		return chosen

	@staticmethod
	def rank(fitness_mappings, ga):
		if ga.fitness_type == 'max':
			new = [i[0] for i in sorted(fitness_mappings, key=operator.itemgetter(1))]
		elif ga.fitness_type == 'min':
			new = [i[0] for i in sorted(fitness_mappings, key=operator.itemgetter(1), reverse = True)]
		elif ga.fitness_type[0] == 'equal':
			new_dict = [(x[0],abs(x[1]-ga.fitness_type[1])) for x in fitness_mappings]
			new = [i[0] for i in sorted(new_dict, key=operator.itemgetter(1), reverse = True)]
		for i in range(len(new)):
			new[i]=(new[i],i+1)
		return SelectionHandlers.roulette(new, ga)

	@staticmethod
	def SUS(fitness_mappings, ga):

		if ga.fitness_type == 'max':
			s_inds = sorted(fitness_mappings, key=operator.itemgetter(1), reverse=True)
		elif ga.fitness_type == 'min':
			s_inds = fitness_mappings
			maxim = (max(s_inds, key = operator.itemgetter(1)))[1]
			for x in range(len(s_inds)):
				s_inds[x] = (s_inds[x][0],maxim - s_inds[x][1])
			s_inds = sorted(fitness_mappings, key=operator.itemgetter(1), reverse=True)
		elif ga.fitness_type[0] == 'equal':
			s_inds = fitness_mappings
			for x in range(len(s_inds)):
				s_inds[x] = (s_inds[x][0],abs(s_inds[x][1] - ga.fitness_type[1]))
			maxim = (max(s_inds, key = operator.itemgetter(1)))[1]
			for x in range(len(s_inds)):
				s_inds[x] = (s_inds[x][0],maxim - s_inds[x][1])
			s_inds = sorted(fitness_mappings, key=operator.itemgetter(1), reverse=True)
		distance = sum([i[1] for i in fitness_mappings]) / float(ga.population.population_size)
		start = random.uniform(0, distance)
		points = [start + i*distance for i in range(len(fitness_mappings)-math.ceil(ga.cross_prob * len(fitness_mappings)))]
		chosen = []
		for p in points:
			i = 0
			sum_ = s_inds[i][1]
			while sum_ < p:
				i += 1
				sum_ += s_inds[i][1]
			chosen.append(s_inds[i][0])
		return chosen


class MutationHandlers:
	"""
	Class contains different  mutation handlers to be invoked by Evolution.py
	module during mutation operation 
	
	Methods :
	---------
	swap() : Performs mutation by swapping genes of chromosome in single point manner

	"""

	@staticmethod
	def swap(chromosome):
		"""
		Performs mutation operation on individual chromomsome by random selecting a
		point on chromosome and the exchanging genes from either side of that point 

		Parameters :
		-----------
		chromosome : List

		Returns :
		---------
		Mutated Chromosome

		"""


		index = random.randint(0,len(chromosome)-2)
		newchrom = copy.copy(chromosome)
		newchrom[index], newchrom[index+1] = newchrom[index+1], newchrom[index]
		return newchrom

	# only when genes are binary
	@staticmethod
	def bitFlip(chromosome):
		index = random.randint(0,len(chromosome)-1)
		chromosome[index] = type(chromosome[index])(not chromosome[index])
		return chromosome

class CrossoverHandlers:
	"""
	Class contains different static methods to be invoked by Evolution.py module  
	during crossover operation
	
	Method :
	-------

	distinct() : performs crossover between to chromosomes by appending genes from one chromosome 
				into other without duplicating the gene present in first chromosome 

	"""

	@staticmethod
	def distinct(chromosome1,chromosome2):
		"""
		Performs crossover between to chromosomes by appending genes from one chromosome 
		into other without duplicating the gene present in first chromosome

		Parameters :
		------------
		chromosome1 : chromosome as one parent
		chromosome2 : chromosome as second parent

		Returns :
		----------
		Tuple containing two new offspring chromosomes produced by crossover 

		"""

		# Need to do some error handling here
		r = random.randint(1,len(chromosome1)-2)
		new_chromosome1 = chromosome1[:r]
		for i in chromosome2:
			if i not in new_chromosome1:
				new_chromosome1.append(i)
		new_chromosome2 = chromosome2[:r]
		for i in chromosome1:
			if i not in new_chromosome2:
				new_chromosome2.append(i)
		return new_chromosome1,new_chromosome2
		
	@staticmethod
	def onePoint(chromosome1, chromosome2):
		size = min(len(chromosome1), len(chromosome2))
		r = random.randint(1, size - 1)
		new_chromosome1 = chromosome1[:r]+chromosome2[r:]
		new_chromosome2 = chromosome2[:r]+chromosome1[r:]
		return new_chromosome1, new_chromosome2

	@staticmethod
	def twoPoint(chromosome1, chromosome2):
		size = min(len(chromosome1), len(chromosome2))
		a = random.randint(1, size - 2)
		b = random.randint(1, size - 1)
		if b==a:
			b+=1
		elif b<a:
			a,b=b,a
		new_chromosome1 = chromosome1[:a]+chromosome2[a:b]+chromosome1[b:]
		new_chromosome2 = chromosome2[:a]+chromosome1[a:b]+chromosome2[b:]
		return new_chromosome1, new_chromosome2
		
	@staticmethod
	def PMX(chromosome1, chromosome2): # Partially Matched Crossover
		size = min(len(chromosome1), len(chromosome2))
		a = random.randint(1, size - 2)
		b = random.randint(1, size - 1)
		if b==a:
			b+=1
		elif b<a:
			a,b=b,a
		new_chromosome1 = chromosome1[:a]+chromosome2[a:b]+chromosome1[b:]
		new_chromosome2 = chromosome2[:a]+chromosome1[a:b]+chromosome2[b:]
		mapping1=chromosome2[a:b]
		mapping2=chromosome1[a:b]
		i = b
		while(i!=a):
			while new_chromosome1[i] in mapping1:
				new_chromosome1[i] = mapping2[mapping1.index(new_chromosome1[i])]
			while new_chromosome2[i] in mapping2:
				new_chromosome2[i] = mapping1[mapping2.index(new_chromosome2[i])]
			i = (i+1)%size
		return new_chromosome1, new_chromosome2
	
	@staticmethod
	def OX(chromosome1, chromosome2): # Ordered Crossover
		size = min(len(chromosome1), len(chromosome2))
		a = random.randint(1, size - 2)
		b = random.randint(1, size - 1)
		if b==a:
			b+=1
		elif b<a:
			a,b=b,a
		new_chromosome1 = [None]*(a)+chromosome1[a:b]+[None]*(size-b)
		new_chromosome2 = [None]*(a)+chromosome2[a:b]+[None]*(size-b)
		i,j,k = b,b,b
		while True:
			if chromosome2[i] not in new_chromosome1:
				new_chromosome1[j] = chromosome2[i]
				j = (j+1)%size
			if chromosome1[i] not in new_chromosome2:
				new_chromosome2[k] = chromosome1[i]
				k = (k+1)%size
			i = (i+1)%size
			if i==b or (j==a and k==a):
				break
		return new_chromosome1, new_chromosome2


class Fitness:
	"""
	Class contains staticmethods for calculating fitness score of an individual 

	Methods :
	--------
	sum() : calculates fitness scores of a candidate

	"""

	@staticmethod

	def addition(chromosome):
		"""
		Calculates fitness score of a chromosome as sum of genes

		Parameters :
		-----------
		chromosome : list
		
		Returns :
		----------
		Fitness score 
		"""
		# print("chromosome in addition = ",chromosome)
		return sum(chromosome)
		
	@staticmethod
	def TSP(chromosome, matrix):
		total = 0
		for i in range(len(chromosome)-1):
			total += matrix[chromosome[i]][chromosome[i+1]]
		return total
