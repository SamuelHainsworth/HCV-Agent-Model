

# import model
# import networkx as nx
#
# graph = model.create_graph("/Users/samhainsworth/Google Drive/HCV Agent Model/Data/LGA_Summary.csv")
#
# print(nx.get_node_attributes(graph, "Hospitals"))
# #
# #
# #
# # print(graph.node[20570]["Undiagnosed"])


import optimise
import model
import time
import networkx as nx
import numpy as np


tmp = time.time()
graph = model.create_graph("/Users/SamuelHainsworth/Google Drive/HCV Agent Model/Data/LGA_Summary.csv")
print(time.time() - tmp)

print(graph.node[10050]['Undiagnosed'])




# tmp = time.time()
# G = mine.create_graph("/Users/samhainsworth/Google Drive/HCV Agent Model/Data/LGA_Summary_TS.csv")
# print(time.time() - tmp)
#
#
# impact = {LGA: value for LGA, value in zip(G.nodes(), range(len(G.nodes())))}
#
# attr = nx.get_node_attributes(G, 'Forecast')
#
# print(attr.items())
# result = {key: (attr[key]["Forecast"] + impact[key]) for key in attr.keys() & impact.keys()}
#
# dict([(key, attr[key] + impact[key]) for key in attr.keys() & impact.keys()])


#attr.update((key, Forecast + adj) for key, Forecast, adj in zip(attr.items(), impact.items() ))
# print(attr.items())

# initialInterventionsDict = {LGA: {Nurses: numNurses, Specialists: numSpec}
#                                     for LGA, Nurses, Specialists, numNurses, numSpec in
#                                     zip(G.nodes(), ['Nurses']*len(G.nodes()), ['Specialists']*len(G.nodes()),
#                                         [3000/len(G.nodes())]*len(G.nodes()),
#                                         [3000/len(G.nodes())]*len(G.nodes())) }
#
# print(initialInterventionsDict)

# forecasts = pd.read_csv("/Users/samhainsworth/Google Drive/HCV Agent Model/Data/arima forecasts by LGA.csv")
# forecasts.columns = ["Date", "LGACode", "Forecast", 'Quarter', "PopSizeImp", "RAName", "AdvantageScore", "NormNotification", "NormPop", "NormAdScore", "DateMonth"]
#
# mapping = {"Major Cities of Australia": 0, "Inner Regional Australia": 0.25,
#                    "Outer Regional Australia": 0.5, "Remote Australia": 0.75,
#                    "Very Remote Australia": 1}
# forecasts.replace({"RAName": mapping}, inplace=True)
#
#
# nurses = mine.distribute_nurses(forecasts)

