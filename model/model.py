import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = {}
        self._grafo = nx.DiGraph()
        self._years = DAO.getAllYears()


    def _crea_grafo(self, anno):
        self._nodes = DAO.getAllNodes(anno)
        self._grafo.add_nodes_from(self._nodes)
        edges = DAO.getAllEdges(anno)
        self._grafo.add_edges_from(edges)

    def get_dettagli_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_predecessors_successors(self, nodo):
        predecessori = self._grafo.predecessors(nodo)
        successori = self._grafo.successors(nodo)
        return predecessori, successori

    def get_comp_connessa(self, nodo):
        #comp_connessa = nx.node_connected_component(self._grafo, nodo)
        # no componente connessa per un grafo orientato con nx
        return []

    def _handle_path(self, partenza):
        self._bestPath = []
        self._ricorsione(partenza, [])
        return self._bestPath

    def _ricorsione(self, nodo, parziale):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)
        successori = self._grafo.successors(nodo)
        for s in successori:
             if self._filtroNodi(s, parziale):
                 parziale.append((nodo, s))
                 self._ricorsione(s, parziale)
                 parziale.pop()

    def _filtroNodi(self, s, parziale):
        for a in parziale:
            if a[0] == s or a[1] == s:
                return False
        return True
