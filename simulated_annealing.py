# uses simulated annealing to optimise the objective function
import numpy as np
from copy import deepcopy as dc
import random
import warnings

def acceptance_prob(oldCost, newCost, temp):
    warnings.filterwarnings("error")    # to catch overflow in exp func

    try:
        prob = np.exp((oldCost - newCost)/temp )
    except RuntimeWarning:
        prob = 1    # definitely accepts

    return prob


def get_neighbours(solutionDict):
    # Produce set of randomly selected neighbours of a given solution

    # random scaling factor
    alpha = np.random.random_sample()

    newSolution = dc(solutionDict)

    lgaList = list(newSolution.keys())
    int1 = random.randint(0, len(lgaList)-1)
    int2 = random.randint(0, len(lgaList)-1)
    # get lga code
    lga1 = lgaList[int1]
    lga2 = lgaList[int2]

    # lga1Nurses = (alpha*lga1Nurses + (1-alpha)*lga2Nurses) etc.
    newSolution[lga1]['Nurses']= newSolution[lga1]['Nurses']*alpha + newSolution[lga2]['Nurses']*(1-alpha)
    newSolution[lga2]['Nurses'] = newSolution[lga2]['Nurses']*alpha + newSolution[lga1]['Nurses']*(1-alpha)

    newSolution[lga1]['Specialists'] = newSolution[lga2]['Specialists']*alpha + newSolution[lga1]['Specialists']*(1-alpha)
    newSolution[lga2]['Specialists'] = newSolution[lga1]['Specialists']*alpha + newSolution[lga2]['Specialists']*(1-alpha)


    return newSolution



def cost(objective_func, **args):

    cost = objective_func(**args)

    return cost



def anneal(objective_func, minTemp=0.0001, alpha=0.8, maxIter=100, **args):
    argCopy = dc(args)
    oldSolution = argCopy['proposedInterventionDict']
    temp = 1

    # get initial objective func value
    oldCost = cost(objective_func, **argCopy)

    for iteration in range(maxIter):
        # stop if cooled
        if temp < minTemp:
            return oldSolution, oldCost

        else:
            newSolution = get_neighbours(argCopy['proposedInterventionDict'] )
            newCost = cost(objective_func, **argCopy)

        # accept with prob 1 if better, < 1 if worse
        if acceptance_prob(oldCost, newCost, temp) > np.random.rand():
            argCopy['proposedInterventionDict'] = newSolution
            oldCost = newCost

        # decrease the temp
        temp = temp*alpha
        print(oldCost)
        print(newCost)



    return argCopy['proposedInterventionDict'], oldCost











