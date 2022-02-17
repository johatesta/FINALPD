from os import system
from Mazo import *

class Jugador:
    """
        ! Para leer esto mas legiblemente podemos instalar BetterComments
        * La clase Jugador contiene sus cartas, una funciona que las muestra y getter de las cartas
        * o carta, tambien con una funcion que descarta cierta carta.
    """
    def __init__(self,cartas):
        self.cartasJugador = cartas
    
    def mostrarCartas(self):
        textoCartas = "----> \t" + "\n----> \t".join(map(str, self.cartasJugador))
        print(textoCartas)

    def getCartas(self):
        return self.cartasJugador

    def getCarta(self,i):
        return self.cartasJugador[i]

    def descartarCarta(self,carta):
        self.cartasJugador.remove(carta)



class Solitario:
     def __init__(self):
        print ("Bienvenido al solitario!")
        self.mazo = Mazo()
        self.puntaje = 0
    

   