from stand import Stand, StandConPrese, StandPremium # vanno importate tutte le classi
from espositore import Espositore
import csv

class LingottoFiere:
    # Tutte le operazioni del menu passano da qui.
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.stand = [] # parametri che verranno inizializzati quando si leggerà il CSV
        # conterrà oggetti Stand, StandConPrese e StandPremium
        self.espositori = []
        # conterrà oggetti Espositore

    """Aggiungere setter e getter se necessari"""
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nuovo_nome):
        self.__nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        # se il file non esiste, open() solleva FileNotFoundError da solo
        # non lo catturo  perché lo gestisce il main
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            righe = csv.reader(file)  # ogni riga arriva già spezzata in una lista di testi
            for riga in righe:
                codice = riga[0]

                # i codici degli stand iniziano con "ST", quelli degli espositori con "ES"
                if codice.startswith("S"):
                    # tipo di stand in base al numero di campi:
                    # 4 campi = standard, 5 campi = con prese o premium
                    if len(riga) == 5:
                        # l'ultimo campo distingue i due tipi:
                        # solo cifre = numero di prese, altrimenti è la posizione
                        if riga[4].isdigit():
                            # dal CSV tutto arriva come str converto in numeri
                            stand_prese = StandConPrese(codice, int(riga[1]), int(riga[2]), float(riga[3]),
                                                        int(riga[4]))
                            self.stand.append(stand_prese)
                        else:
                            stand_premium = StandPremium(codice, int(riga[1]), int(riga[2]), float(riga[3]), riga[4])
                            self.stand.append(stand_premium)
                    else:
                        standard = Stand(codice, int(riga[1]), int(riga[2]), float(riga[3]))
                        self.stand.append(standard)
                else:
                    # tutto ciò che non è uno stand è un espositore
                    espositore = Espositore(codice, riga[1], riga[2])
                    self.espositori.append(espositore)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        # CONTROLLO 1 lo stand esiste?
        stand_trovato = None  # None = "non ho ancora trovato niente"
        for s in self.stand:
            if s.codice == codice_stand:
                stand_trovato = s

        if stand_trovato is None:
            raise Exception(f"Stand {codice_stand} non esistente") # raise interrompe il metodo

        # CONTROLLO 2 l'espositore esiste?
        espositore_trovato = None
        for e in self.espositori:
            if e.codice == codice_espositore:
                espositore_trovato = e

        if espositore_trovato is None:
            raise Exception(f"Espositore {codice_espositore} non esistente")

        # CONTROLLO 3 lo stand è libero?
        if not stand_trovato.disponibile:
            raise Exception(f"Stand {codice_stand} non disponibile")

        # CONTROLLO 4 l'espositore ha già uno stand?
        if espositore_trovato.assegnazione is not None:
            raise Exception(f"Espositore {codice_espositore} ha già uno stand assegnato")

        # i controlli sono passati aggiorno ENTRAMBI i lati della relazione
        stand_trovato.disponibile = False
        stand_trovato.assegnazione = espositore_trovato
        espositore_trovato.assegnazione = stand_trovato

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for e in self.espositori:
            print(e)
            # richiama il __str__ di Espositore, che mostra lo stand solo se assegnato

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand)
        # sorted() crea una nuova lista e confronta gli stand con __lt__ (definito in stand.py),
        # che usa il prezzo FINALE di ciascun tipo. Restituisco, non stampo quello lo fa il main
