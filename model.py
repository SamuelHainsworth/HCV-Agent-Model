import numpy as np
import pandas as pd
import networkx as nx
import subprocess
from scipy import optimize

class Resources:
    # in charge of tracking the resources at our disposal
    # TODO get the constants below
    def __init__(self, funds=1000000, nurses=10000, specialists=10000):
        self.funds = funds
        self.nurses = nurses    # TODO want nurses + specialists to be a function of available funds?
        self.specialists = specialists


    def cost(self, intervention):
        # calc cost of an intervention
        # TODO estimate cost

        return

class Medical:
    # keeps track of medical things
    # TODO get the constants below
    def __init__(self, testRate=1, testCoverage=1, undiagnosed=40543, treatmentCoverage=1, nurseEffectiveness=0.5, specialistEffectiveness=0.5, expectedNewInfections=11000):
        self.testrate = testRate
        self.testcoverage = testCoverage
        self.undiagnosed = undiagnosed  # Kirby surveillance report 2016
        self.untreated = 0
        self.treatmentCoverage = treatmentCoverage
        self.nurseEffectiveness = nurseEffectiveness
        self.specialistEffectiveness = specialistEffectiveness
        self.expectedNewInfections = expectedNewInfections

    def nurse_effectiveness(self, numNurses, undiagnosed, GPs, hospitals, specialists, drugServices, NSPs):
        #TODO steepness should be a function of undiagnosed, healthcare services, testing rate (access self.testrate) & test coverage

        steepness = 0.05 #GPs + hospitals + specialists + drugServices + NSPs

        percentageIncrease = lambda x: 2/(1 + np.exp(-steepness * x)) - 1


        return percentageIncrease(numNurses)

    def educator_effectiveness(self, numEducators, undiagnosed, GPs, hospitals, specialists, drugServices, NSPs):
        # TODO steepness should be a function of undiagnosed, healthcare services, testing rate (access self.testrate) & test coverage

        steepness = 0.05  # GPs + hospitals + specialists + drugServices + NSPs

        percentageIncrease = lambda x: 2/(1 + np.exp(-steepness * x)) - 1

        return percentageIncrease(numEducators)



    def intervention_impact(self, proposedInterventionsDict, medicalServices, lgacodes):
        '''
        Calculates the impact on number of notifications given specific interventions
        :return: impact, a dictionary of scalars where key is lga code and scalar is number of new notifications
        '''

        # Get impact of nurses + educators, then combine for overall impact per LGA
        for lga, distribution in proposedInterventionsDict.items():
            numNurses = distribution['Nurses']
            numEducators = distribution["Specialists"]
            undiagnosed = medicalServices["Undiagnosed"]
            args = { 'GPs': medicalServices['GPs'][lga], 'hospitals': medicalServices['Hospitals'][lga],
                     'specialists': medicalServices['Specialists'][lga], 'drugServices': medicalServices['DrugServices'][lga],
                     'NSPs': medicalServices['NSPs'][lga]}
            nursePercentageIncrease = self.nurse_effectiveness(numNurses, undiagnosed, **args)
            educatorPercentageIncrease = self.educator_effectiveness(numEducators, undiagnosed, **args)

            # TODO combine these impacts



        # TEST VALUES ONLY
        impact = {LGA: value for LGA, value in zip(lgacodes, np.random.randint(0, 20, len(lgacodes)))}

        return impact

    def num_treated(self, notified, numNurses, numEducators, medicalServices):
        '''
        :param notified: the number of people notified
        :return: a scalar of the number treated
        '''
        # TODO the number treated is a function of existing resources, new nurses & educators


        #treated = notified*self.nurseEffectiveness #*numNurses

        # TEST VALUE ONLY
        treated = notified * 0.6

        return treated





def get_notifications(forecasts, impact, quarter, numQuarters=0, simple=True):
    '''
    Calculates the notifications for all LGAs by combining forecast output with manually
    estimated effects for nurse efficiency.
    :param quarter: The quarter for which notifications forecast is desired.
    :param forecasts: data frame containing forecasts for all LGAs
    :param simpe: boolean. If True then only uses an additive model of notification adjustment.
    :return: notification count adjusted by estimated intervention impact
    '''



    # additive forecasting
    if simple:
        # TODO sum must be less than medical.undiagnosed
        # adds impact by lga code (key)
        adjusted_forecasts = {key: (forecasts[key]["Forecast"] + impact[key]) for key in forecasts.keys() & impact.keys()}

    else:
        # TODO no other method yet
        pass



    return adjusted_forecasts


def create_graph(filePath, reforecast = False, numQuarts = 8):
    '''
    :return: a set of nodes with populated attributes
    '''
    # check if file exists
    try:
        df = pd.read_csv(filePath)
    except FileNotFoundError:
        print("Wrong file or file path")
        return

    else:
        # get forecast data set
        if reforecast:
            pass
            # get new forecast. Will be identical to old forecast unless other work is done to change method/data
            # forecasts = forecast(num_quarters)
        else:
            # load previously forecasted data
            forecasts = pd.read_csv("/Users/samhainsworth/Google Drive/HCV Agent Model/Data/arima forecasts by LGA.csv")


        # TODO may need to add distances between LGAs for interacting terms

        # initialise graph
        G = nx.Graph()
        for lga in np.unique(df[["LGACode"]]):    # iterate over the unique LGAs in df to create node
            # name of node is lga code. it is unique
            G.add_node(lga,
                       Name = df.loc[(df["Date"] == "2016 Q1") & (df["LGACode"] == lga), "LGAName"].values[0],
                       NSPs = df.loc[(df["Date"] == "2016 Q1") & (df["LGACode"] == lga), "NSPs"].values[0],
                       BusinessNSPs = df.loc[(df["Date"] == "2016 Q1") & (df["LGACode"] == lga), "NSPsBusHours"].values[0],
                       GPs = df.loc[(df["Date"] == "2015 Q1") & (df["LGACode"] == lga), "GPs"].values[0],
                       DrugServices = df.loc[(df["Date"] == "2015 Q1") & (df["LGACode"] == lga), "DrugAlcoholServices"].values[0],
                       Hospitals = df.loc[(df["Date"] == "2015 Q1") & (df["LGACode"] == lga), "Hospitals"].values[0],
                       Specialists = df.loc[(df["Date"] == "2015 Q1") & (df["LGACode"] == lga), "Specialists"].values[0],
                       Prisons = df.loc[(df["Date"] == "2016 Q1") & (df["LGACode"] == lga), "Prisons"].values[0],
                       RA = df.loc[(df["Date"] == "2016 Q1") & (df["LGACode"] == lga), "RA"].values[0],
                       ProportionAboriginal = df.loc[(df["Date"] == "2016 Q1") & (df["LGACode"] == lga), "PropAboriginal"].values[0],
                       ProportionBornOverseas = df.loc[(df["Date"] == "2016 Q1") & (df["LGACode"] == lga), "PropBornOverseas"].values[0],
                       AdvantageScore = df.loc[(df["Date"] == "2016 Q1") & (df["LGACode"] == lga), "AdvantageScore"].values[0],
                       TSData = df.loc[df["LGACode"] == lga, [ "Date", "LGACount", "PopulationSize"]],
                       Forecast = forecasts.loc[forecasts["LGACode"] == lga])

        # distribute undiagnosed & incidence to LGAs on population basis (use most recent pop)
        medical = Medical()
        for lga in G.nodes_iter():
            data = G.node[lga]['TSData']
            popSizeProportion = data.loc[(data["Date"] == "2015 Q1"), "PopulationSize"].values[0] / 23968973    # divide by Aus pop size in 2015
            G.node[lga]['Undiagnosed'] = popSizeProportion * medical.undiagnosed
            G.node[lga]['ExpectedNewInfections'] = popSizeProportion * medical.expectedNewInfections



        return G
















