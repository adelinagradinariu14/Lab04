class Espositore:
    # lo stand conosce il suo espositore, e l’espositore conosce il suo stand = doppio verso
    # (li aggiorna assegna_stand_a_espositore)
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.assegnazione = None # non presente nel CSV,
        # avrà l'oggetto intero Stand (con tutti i suoi attributi), quando verrà assegnato

    def stato(self):
        # scrivo il testo dello stato così __str__ lo riusa senza ripetere l'if
        if self.assegnazione is None:
            return "Nessuno stand assegnato"
        return f"Stand assegnato: {self.assegnazione.codice}"

    def __str__(self):
        return f"{self.codice}: {self.nome} {self.cognome} - {self.stato()}"
