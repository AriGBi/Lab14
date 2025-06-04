import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph= nx.DiGraph()
        self.idMap={}
        self._bestPath=[]
        self._bestCost=0

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


    def getPercorsoOttimo(self, nodoPartenza):
        self._bestPath = []
        self._bestCost = 0
        parziale=[nodoPartenza]
        esplorabili=list(self.graph.successors(nodoPartenza))
        self.ricorsione(parziale,esplorabili)
        return self._bestPath, self._bestCost

    def ricorsione(self, parziale,esplorabili):
        #condizione termine
        if len(esplorabili)==0:
            if (self.calcolaCosto(parziale)>self._bestCost):
                self._bestCost=self.calcolaCosto(parziale)
                self._bestPath = copy.deepcopy(parziale)
        else:
            for nodo in esplorabili:
                if nodo not in parziale:
                    parziale.append(nodo)
                    nuovoEsplorabili= self.calcolaEsplorabili(nodo, parziale)
                    self.ricorsione(parziale, nuovoEsplorabili)
                    parziale.pop()


    def calcolaEsplorabili(self, nodo, parziale):
        esplorabili=[]
        for nodo2 in list(self.graph.successors(nodo)):
            if nodo2 not in parziale:
                if self.graph[parziale[-1]][nodo2]["weight"]< self.graph[parziale[-2]][parziale[-1]]["weight"]:
                    esplorabili.append(nodo2)
        return esplorabili

    def calcolaCosto(self,lista):
        costo=0
        for i in range(0,len(lista)-1):
            costo+=self.graph[lista[i]][lista[i+1]]["weight"]
        return costo


