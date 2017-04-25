# The one script to rule them all
# Seek model simulations within

import optimise
import model as model


if __name__ == "__main__":
    def run_model():
        path = "/Users/samhainsworth/Google Drive/HCV Agent Model/Data"
        graph = model.create_graph(filePath = path)

        optimalSol, optimalCost = optimise.optimise_func(graph)

        return optimalSol, optimalCost


    output = run_model()
    print(output[0])
    print(output[1])
























