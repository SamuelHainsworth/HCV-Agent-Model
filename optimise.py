import model
import numpy as np
import networkx as nx
import simulated_annealing as sim_anneal


def objective_func(proposedInterventionDict, forecasts, resources, medical, medicalServices, alpha = 1, beta = 1):
    '''
    The function to be minimised.
    
    :param proposedInterventionDict: Nested dictionary with lga code as outer key ('LGA'), then inner key being 'Nurses' or 'Specialists' giving raw number present
    :param resources: an object containing resource information
    :param alpha: the weighting to be given to the number of undiagnosed
    :param beta: weighting to be given the number of untreated
    :return: a scalar which is the weighted sum of undiagnosed & untreated people
    '''

    # calculate impact of proposed intervention
    impact = medical.intervention_impact(proposedInterventionDict, medicalServices, list(forecasts.keys()))
    # use impact to get adjusted notifications
    adjusted_notifications = model.get_notifications(forecasts, impact, quarter=1)
    # update undiagnosed, number on treatment
    notifs = list(adjusted_notifications.values())
    sums = [x.sum() for x in notifs]
    totalNotifications = sum(sums)

    # TODO cannot allow undiagnosed to go below 0

    undiagnosed = (medical.undiagnosed + medical.expectedNewInfections) - totalNotifications
    # TODO calc nurse effectiveness for treatments
    untreated = totalNotifications - medical.num_treated(totalNotifications, resources.nurses, resources.specialists, medicalServices)


    return alpha*undiagnosed + beta*untreated


def optimise_func(graph):
    '''
    :param graph:
    :return:
    '''
    resources = model.Resources()
    medical = model.Medical()

    # for initial run
    LGAs = graph.nodes()
    numLGAs = len(LGAs)
    # random lists
    randList1 = np.random.rand(numLGAs)
    randList1 /= sum(randList1)
    randList2 = np.random.rand(numLGAs)
    randList2 /= sum(randList2)

    proposedInterventionDict = {LGA: {Nurses: numNurses, Specialists: numSpec}
                                    for LGA, Nurses, Specialists, numNurses, numSpec in
                                    zip(LGAs, ['Nurses']*numLGAs, ['Specialists']*numLGAs,
                                        resources.nurses*randList1,
                                        resources.specialists*randList2)}

    # get all the required lga medical features
    medicalList = ["GPs", "Specialists", "Hospitals", "DrugServices", "NSPs", "Undiagnosed", "ExpectedNewInfections"]
    # dictionary to store
    medicalDict = {}

    for feature in medicalList:
        # assign all medical features to dictionary
        medicalDict[feature] = nx.get_node_attributes(graph, feature)

    # get forecasts separately
    forecasts = nx.get_node_attributes(graph, "Forecast")

    args = {'proposedInterventionDict': proposedInterventionDict, 'forecasts': forecasts,
            'resources': resources, 'medical': medical,
            'medicalServices': medicalDict}

    #### Run optimisation
    optimalSolution, optimalCost = sim_anneal.anneal(objective_func, **args)


    return optimalSolution, optimalCost





