from flask import Flask, render_template, url_for, flash, redirect,request
from forms import PyGeneticForm

from GAEngine import *
from Utils import *
from ChromosomeFactory import *
from Population import *

import sys


sys.path.append('C:/pygenetic')

from pyGenetic import *
# import pyGenetic

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/",methods=['GET','POST'])
def pygenetic():

    if request.method == "GET":
        form = PyGeneticForm()
        return render_template('pygenetic.html',title='Pygenetic',form=form)

    elif request.method == "POST":
        return generate_and_run()



def generate_and_run():

    #chromosome = request.form['chromosome']
    fitness_threshold = request.form['fitness_threshold']
    #factory = request.form['factory']
    population_size = request.form['population_size']
    #crossover_probability = request.form['crossover_probability']
    maximum_iterations = int(request.form['maximum_iterations'])
    #mutation_probability = request.form['mutation_probability']
    #adaptive_mutation = request.form['adaptive_mutation']
    #smart_fitness = request.form['smart_fitness']

    import copy
    factory = ChromosomeFactory.ChromosomeRangeFactory(int,8,1,9)
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

    ga = GAEngine(fitness,8,factory,10)



    ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct)
    ga.addMutationHandler(Utils.MutationHandlers.swap)
    ga.setSelectionHandler(Utils.SelectionHandlers.basic)
    ga.evolve(maximum_iterations)

    '''
    genes_per_chromosome = request.form['no_of_genes']
    crossover_prob = request.form['crossover_probability']
    mutation_prob = request.form['mutation_probability']
    population_size = request.form['population_size']
    fitness_func = request.form['fitness_function']
    max_iteration = request.form['maximum_iterations']
    crossover_type = request.form['crossover_type']
    mutation_type = request.form['mutation_type']
    selection = request.form['selection_type']

    ga = new GAEngine(chromosome, fitness_threshold, factory , population_size,
                        crossover_probability, mutation_probability, adaptive_mutation,
                        smart_fitness)
    '''
    return "sdklfj"

if __name__ == '__main__':
    app.run(debug=True)
