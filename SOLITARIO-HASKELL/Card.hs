

module Card 
(Color(..),
Suit(..),
Rank(..),
Card(..),
Move(..),
cardColor,
cardValue,
removeCard,
allSameColor,
sumCards,
score)
where 
import System.IO

import Data.List
import Text.XHtml (face)
--import System.Random


data Color = Red | Black
	deriving (Show, Eq)

data Suit = Clubs | Diamonds | Hearts | Spades
	deriving (Show, Eq)

data Rank = Num Int | Jack | Queen | King | Ace
	deriving (Show, Eq)

data Card = Card { suit :: Suit, rank :: Rank }
	deriving (Show, Eq)

data Move = Draw | Discard Card
	deriving (Show, Eq)


cardColor :: Card -> Color
cardColor card = case suit card of
	Clubs  -> Black
	Spades -> Black
	_      -> Red
	

cardValue :: Card -> Integer
cardValue card
	| r == Ace                             = 11
	| r == Jack || r == Queen || r == King = 10
	| otherwise                            = read (show r) :: Integer
	where
		r = rank card


removeCard :: Card -> [Card] -> [Card]
removeCard _ [] = error "card is not in list"
removeCard c (c':cs) = if c == c' then cs else c':removeCard c cs


allSameColor :: [Card] -> Bool
allSameColor cs = case cs of
	[]           -> True  -- can be changed
	[_]          -> True
	c1:cs@(c2:_) -> if cardColor c1 /= cardColor c2 then False else allSameColor cs


sumCards:: [Card] -> Integer
sumCards cs = sum' 0 cs
	where
		sum' :: Integer -> [Card] -> Integer
		sum' acc cards
			| null cards = acc
			| otherwise  = sum' (acc + cardValue (head cards)) (tail cards)


score :: [Card] -> Integer -> Integer
score hand goal
	| allSameColor hand = floor ((fromIntegral $ preliminary hand  goal) / 2.0)
	| otherwise         = preliminary hand goal
	where
		preliminary :: [Card] -> Integer -> Integer
		preliminary hand goal = if sum > goal then 3*(sum-goal) else goal-sum
			where
				sum = sumCards hand
