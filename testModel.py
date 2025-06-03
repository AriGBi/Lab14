from model.model import Model

myModel=Model()
nodi, archi=myModel.buildGraph(1, 5)
print(len(nodi), len(archi))
