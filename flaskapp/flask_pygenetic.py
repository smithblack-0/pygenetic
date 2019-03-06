from flask import Flask, render_template, url_for, flash, redirect,request
from forms import PyGeneticForm
import sys, os , io
from os import path
from GAEngine import *
from Utils import *
from ChromosomeFactory import *
from Utils import *
import matplotlib.pyplot as plt

#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#from pyGenetic import GAEngine, Population, ChromosomeFactory, Utils


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/",methods=['GET','POST'])
def pygenetic():

    if request.method == "GET":
        form = PyGeneticForm()
        return render_template('pygenetic.html',title='Pygenetic',form=form)

    elif request.method == "POST":
        results = generate_and_run()
        return render_template('result.html', title = 'Result', results = results)



def generate_and_run():

    #chromosome = request.form['chromosome']
    fitness_threshold = request.form['fitness_threshold']
    #factory = request.form['factory']
    population_size = int(request.form['population_size'])
    #crossover_probability = float(request.form['crossover_probability'])
    maximum_iterations = int(request.form['maximum_iterations'])
    #mutation_probability = float(request.form['mutation_probability'])
    #fitness_func = request['fitness_func']
    #adaptive_mutation = request.form['adaptive_mutation']
    #smart_fitness = request.form['smart_fitness']

    factory = ChromosomeRangeFactory(int,8,1,9)
    import copy



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


    #ga = GAEngine(fitness, fitness_threshold ,factory,population_size, crossover_probability, mutation_probability)
    ga = GAEngine(fitness, fitness_threshold ,factory,population_size)
    ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct)
    ga.addMutationHandler(Utils.MutationHandlers.swap)
    ga.setSelectionHandler(Utils.SelectionHandlers.basic)
    all_iterations_result = ga.evolve(maximum_iterations)
    return all_iterations_result

    #return "sdklfj"

if __name__ == '__main__':
    app.run(debug=True)
