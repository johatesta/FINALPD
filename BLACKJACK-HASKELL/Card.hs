module Cards
(
  Card(..),
  Deck,
  Hand(..),
  score,
  getDeck,
  containsAce,
  blackjack
) where


data Card = Ace | Dos | Tres | Cuatro | Cinco | Seis | Siete | Ocho | Nueve |
            Diez | Jack | Queen | King deriving (Show, Eq, Enum)
type Hand = [Card]
type Deck = [Card]

getSuit :: [Card]
getSuit = [Dos, Tres, Cuatro, Cinco, Seis, Siete, Ocho, Nueve, Diez,
           Jack, Queen, King, Ace]

-- 1 deck = 4 suits
getDeck :: Deck
getDeck = foldl (\acc x -> acc ++ getSuit) [] [1..4]

-- lay out the values for each card
value :: Card -> Int
value Dos = 2
value Tres = 3
value Cuatro = 4
value Cinco = 5
value Seis = 6
value Siete = 7
value Ocho = 8
value Nueve = 9
value Diez = 10
value Jack = 10
value Queen = 10
value King = 10
value Ace = 11

-- externally callable scoring function; calls scoreHeper with an initial
-- count of 0 soft Aces
score :: Hand -> Int
score h = scoreHelper h 0

-- calculates the highest non-bust score, or the lowest bust score if the
-- player is guaranteed to bust
scoreHelper :: Hand -> Int -> Int
scoreHelper [] numSoftAces = numSoftAces
scoreHelper h@(head:tail) numSoftAces
  | (value head + scoreHelper tail numSoftAces) > 21 && containsAce h =
    scoreHelper (popAce h) (numSoftAces + 1)
  | otherwise = value head + scoreHelper tail numSoftAces

-- return true if the hand contains an Ace
containsAce :: Hand -> Bool
containsAce [] = False
containsAce h@(head:tail)
  | head == Ace = True
  | otherwise = containsAce tail

-- take the given hand and remove one Ace
popAce :: Hand -> Hand
popAce [] = []
popAce h@(head:tail)
  | head == Ace = tail
  | otherwise = head : popAce tail

-- determine whether the hand is a blackjack
blackjack :: Hand -> Bool
blackjack h
  | score h == 21 && length h == 2 = True
  | otherwise = False