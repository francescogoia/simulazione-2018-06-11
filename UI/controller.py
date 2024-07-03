import time

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selected_year = None
        self._selected_state = None




    def fillDDAnno(self):
        years = self._model._years
        for y in years:
            self._view._DD_anno.options.append(ft.dropdown.Option(data=y[0], text=f"{y[0]}, numAvvistamenti = {y[1]}", on_click=self._choice_year))
        self._view.update_page()


    def _choice_year(self, e):
        if e.control.data is None:
            self._selected_year = None
        else:
            self._selected_year = e.control.data

    def fillDDStato(self):
        states = self._model._nodes
        for s in states:
            self._view._DD_stato.options.append(ft.dropdown.Option(data=s, text=s.upper(), on_click=self._choice_state))
        self._view.update_page()

    def _choice_state(self, e):
        if e.control.data is None:
            self._selected_state = None
        else:
            self._selected_state = e.control.data
            self._view._btn_sequenza.disabled = False
            self._view.update_page()


    def handleGrafo(self, e):
        if self._selected_year != None:
            self._model._crea_grafo(self._selected_year)
            nNodi, nArchi = self._model.get_dettagli_grafo()
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text(f"Grafo correttamente creato.\n"
                                                           f"Il grafo ha {nNodi} nodi e {nArchi} archi."))
            self._view._DD_stato.disabled =False
            self._view._btn_analizza.disabled = False
            self.fillDDStato()
            self._view.update_page()
        else:
            self._view.txt_result1.controls.append(ft.Text(f"Errore, selezionare un anno."))
            self._view.update_page()
            return

    def handleAnalizza(self, e):
        predecessori, successori = self._model.get_predecessors_successors(self._selected_state)
        self._view.txt_result1.controls.append(ft.Text(f"Nodi predecessori di {self._selected_state}: "))
        for p in predecessori:
            self._view.txt_result1.controls.append(ft.Text(f"{p.upper()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Nodi successori di {self._selected_state}: "))
        for s in successori:
            self._view.txt_result1.controls.append(ft.Text(f"{s.upper()}"))
        comp_connessa = self._model.get_comp_connessa(self._selected_state)
        self._view.txt_result1.controls.append(ft.Text(f"Componente connessa di {self._selected_state}: "))
        # non esiste la componente connessa di un grafo orientato
        for c in comp_connessa:
            self._view.txt_result1.controls.append(ft.Text(f"{c.upper()}"))
        self._view.update_page()


    def handleSequenza(self, e):
        if self._selected_state != None:
            path = self._model._handle_path(self._selected_state)
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Trovato percorso lungo {len(path)}:"))
            for p in path:
                self._view.txt_result2.controls.append(ft.Text(f"{p[0].upper()} --> {p[1].upper()}"))
        else:
            self._view.txt_result2.clear()
            self._view.txt_result2.append(ft.Text(f"Errore, selezionare uno stato di partenza."))
            self._view.update_page()
            return
        self._view.update_page()




