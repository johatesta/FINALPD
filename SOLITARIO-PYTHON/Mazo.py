import random


class Carta:
    def __init__(self,valor, palo):
        self.valor = valor
        self.palo = palo

    def getValor(self):
        return self.valor

    def getPalo(self):
        return self.palo

    def __repr__(self) -> str:
        return " de ".join((self.valor,self.palo))


class Mazo:
    Valor = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
             'Jack', 'Queen', 'King']
    Palo = ['Hearts', 'Clubs', 'Diamonds', 'Spades']

    def __init__(self):
        # self.mazo = [Carta(v,p) for v in self.VALORES for p in self.PALOS ]
        self.mazo = [Carta(v,p) for p in self.PALOS for v in self.VALORES ]

    def showMazo(self):
        if len(self.mazo) > 0:
            print(self.mazo)

    def mezclarMazo(self):
        if len(self.mazo) > 1:
            random.shuffle(self.mazo)
    
    def darCartas(self,i):
        return self.mazo[-i:]

    def descartarCartas(self,i):
        self.mazo = self.mazo[:len(self.mazo) - i]