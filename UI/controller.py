import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDD=None
        self._nodi=None
        self.nodoPartenza=None



    def handleCreaGrafo(self, e):
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare uno store"))
            self._view.update_page()
            return
        giorno=self._view._txtIntK.value
        if giorno=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, scegliere un numero massimo di giorni"))
            self._view.update_page()
            return
        try:
            giornoInt=int(giorno)

        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserisci un numero intero"))
            self._view.update_page()
            return
        self.nodi,archi=self._model.buildGraph(self._choiceDD.store_id,giornoInt)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente."))
        self._view.txt_result.controls.append(ft.Text(f" Numero nodi: {len(self.nodi)}"))
        self._view.txt_result.controls.append(ft.Text(f" Numero archi: {len(archi)}"))
        self.fillDD2()
        self._view.update_page()
        return

    def fillDD2(self):
        self._view._ddNode.options.clear()
        for nodo in self.nodi:
            self._view._ddNode.options.append(ft.dropdown.Option(text=nodo.order_id, data=nodo, on_click=self.readDD2))
        self._view.update_page()

    def readDD2(self,e):
        self.nodoPartenza=e.control.data


    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        percorsoOttimo, costoOttimo=self._model.getPercorsoOttimo(self.nodoPartenza)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Percorso ottimo trovato. Esso attravera {len(percorsoOttimo)} nodi e ha costo {costoOttimo}"))
        self._view.update_page()

    def fillDD(self):
        stores= self._model.getAllStores()
        for store in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(text=store.store_name, data=store, on_click=self.readDD))
        self._view.update_page()

    def readDD(self,e):
        self._choiceDD=e.control.data
