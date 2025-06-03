import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph= nx.DiGraph()
        self.idMap={}

    def buildGraph(self, store_id, maxGiorni):
        self.graph.clear()
        nodes=list(DAO.getAllNodes(store_id))
        for n in nodes:
            self.graph.add_node(n)
            self.idMap[n.order_id]=n
        archi= DAO.getAllArchi(maxGiorni,store_id, self.idMap)
        for arco in archi:
            self.graph.add_edge(arco.nodo1, arco.nodo2, weight=arco.peso)
        return self.graph.nodes, self.graph.edges

    def getAllStores(self):
        return DAO.getAllStores()

