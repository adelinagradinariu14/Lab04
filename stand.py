# classe madre (stand Standard) e due classi figlie

class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = superficie
        self.padiglione = padiglione
        self.prezzo_base = prezzo_base
        # questi due dati non arrivano dal CSV, uno stand nuovo è libero e senza espositore
        self.disponibile = True
        self.assegnazione = None # conterrà l'oggetto Espositore quando verrà assegnato

    def prezzo_finale(self):
        # lo Standard non ha sovrapprezzi
        return self.prezzo_base

    def stato(self):
        # restituisce il testo giusto in base a self.disponibile
        # lo scrivo una volta sola, le figlie poi lo ereditano e lo usano
        if self.disponibile:
            return "Disponibile"
        return "Non disponibile"

    def __str__(self):
        return (f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} "
                f"- Prezzo {self.prezzo_finale():.2f}€ - {self.stato()}")

    # metodo per ordinare gli stand in base al prezzo
    def __lt__(self, other):
        return self.prezzo_finale() < other.prezzo_finale()

class StandConPrese(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, prese):
        super().__init__(codice, superficie, padiglione, prezzo_base) # dati comuni, chiama l'init della madre
        self.prese = prese

    def prezzo_finale(self):
        # +7% per ogni presa extra, polimorfismo
        return self.prezzo_base * (1 + 0.07 * self.prese)

    def __str__(self):
        return (f"{self.codice}: Prese Extra | {self.superficie} mq - Padiglione {self.padiglione} "
                f"- Prezzo {self.prezzo_finale():.2f}€ - Prese aggiuntive: {self.prese} - {self.stato()}")

class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def prezzo_finale(self):
        # sovrapprezzo del 30%, polimorfismo
        return self.prezzo_base * 1.30

    def __str__(self):
        return (f"{self.codice}: Premium | {self.superficie} mq - Padiglione {self.padiglione} "
                f"- Prezzo {self.prezzo_finale():.2f}€ - Posizione: {self.posizione} - {self.stato()}")

