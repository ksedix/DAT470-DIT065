#!/usr/bin/env python3

import numpy as np
import numpy.typing as npt
import random
import argparse
from enum import Enum
from typing import List, Tuple, Callable, Optional
from itertools import product
import time

class Suit(Enum):
    """
    Enum for French-suited playing cards
    """
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

    

class Rank(Enum):
    """
    Enum for card rank in French-suited playing cards
    """
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


    
class Card:
    """
    One card in the French-suited playing cards
    """

    _suit: Suit
    _rank: Rank

    def __init__(self, suit: Suit, rank: Rank):
        self._suit = suit
        self._rank = rank

    def __repr__(self)->str:
        suit: str = ''
        if self._suit == Suit.CLUBS:
            suit = 'clubs'
        elif self._suit == Suit.DIAMONDS:
            suit = 'diamonds'
        elif self._suit == Suit.HEARTS:
            suit = 'hearts'
        elif self._suit == Suit.SPADES:
            suit = 'spades'
        rank: str = ''
        if self._rank == Rank.ACE:
            rank = 'ace'
        elif self._rank == Rank.JACK:
            rank = 'jack'
        elif self._rank == Rank.QUEEN:
            rank = 'queen'
        elif self._rank == Rank.KING:
            rank = 'king'
        else:
            rank = f'{self._rank.value}'

        return f'{rank} of {suit}'


    
class Deck:
    """
    A simple (albeit inefficient) class depicting a deck of 
    cards.
    Cards can be drawn from the deck one at a time.
    Shuffling the shoe resets its state (all cards are returned to the deck, as
    it were)
    """
    
    _cards: List[Card] # internal representation
    _current: int # current card
    def __init__(self, shuffle: bool = True):
        """
        Constructs a deck of cards.
        Parameters:
        - shuffle: if True, automatically shuffles the deck upon construction.
        """
        self._cards = [Card(suit,rank) for (suit,rank) in product(Suit,Rank)]

        if shuffle:
            self.shuffle()

        self._current = 0

    def shuffle(self):
        """
        Shuffles the deck
        """
        random.shuffle(self._cards)
        self._current = 0

    def draw(self)->Card:
        """
        Draws one card from the shoe, advances the state.
        """
        assert self._current < len(self._cards)
        self._current += 1
        return self._cards[self._current-1]


    

class Decision(Enum):
    """
    Possible decisions in a game of blackjack
    """
    HIT = 1 # take another card
    STAND = 2 # take no more cards


    
# represents the strategy function (takes a hand and the dealer card, returns a decision)
strategy_type = Callable[[List[Card],Card], Decision]


    
def hand_value(hand: List[Card])->int:
    """
    Computes the value of the hand according to Blackjack rules:
    - Ace is 1/11 (whichever choice brings the greatest value not 
    exceeding 21)
    - Jacks, queens, and kings are valued 10
    - All other cards have their rank value
    
    Parameters:
    - hand: the hand in question
    """
    aces: int = 0
    s: int = 0
    for card in hand:
        if card._rank == Rank.ACE:
            aces += 1
        elif card._rank == Rank.JACK:
            s += 10
        elif card._rank == Rank.QUEEN:
            s += 10
        elif card._rank == Rank.KING:
            s += 10
        else:
            s += card._rank.value
    if aces > 1:
        s += aces-1
        aces = 1
    if aces*11 + s <= 21:
        return aces*11 + s
    else:
        return aces + s


    
def play_hand(deck: Deck, hand: List[Card], strategy: strategy_type,
                  dealer_card: Card):
    """
    Plays a single hand according to the strategy.
    
    Parameters:
    - deck: the deck to use
    - hand: the hand to play (modified in-place)
    """
    # regardless of what player wants to do, they must stand at 21
    while hand_value(hand) < 21:
        decision = strategy(hand, dealer_card)
        if decision == Decision.HIT:
            # player takes a card and continues
            hand.append(deck.draw())
        else:
            assert decision == Decision.STAND
            # player takes no more cards
            break



def dealer_strategy(hand: List[Card], dealer: Card)->Decision:
    """
    The dealer follows the following deterministic strategy:
    - if the value of the hand is at most 16, hit
    - if the value of hand is at least 17, stand
    This is also known as a 'stand on soft-17' strategy.
    
    Parameters:
    - hand: Dealer's hand (including the hole card)
    - dealer: ignored, only used for consistency
    """
    value = hand_value(hand)
    if value < 17:
        return Decision.HIT
    else:
        return Decision.STAND

    
    
def play_blackjack(strategy: strategy_type, bet: float = 1.0)->float:
    """
    Play a single deal of Blackjack.
    Parameters:
    - strategy: player strategy
    - bet: amount to bet (by default 1.0 for "one unit")
    
    Returns the gains/losses (so a win 1:1 returns 1.0, a loss -1.0, 
    a tie 0.0, and a blackjack 3:2 returns 1.5)
    """
        
    # The game has the following steps:
    # 1. two cards are dealt to the player and the dealer
    # 2. we resolve whether the player and/or the dealer has a blackjack
    # 3. the player plays according to his/her strategy
    # 4. if the player goes bust, he/she loses immediately
    # 5. the dealer plays according to his/her strategy
    # 6. if the dealer busts, he/she loses immediately
    # 7. wins are resolved
        
    # start by creating a shuffled deck
    deck: Deck = Deck()
        
    # deal cards to the player
    player_hand: List[Card] = [deck.draw(), deck.draw()]
        
    # dealer draws two cards
    dealer_card: Card = deck.draw() # dealer's face-up
    hole_card: Card = deck.draw() # the hole card, not shown to the player
    dealer_hand: List[Card] = [dealer_card, hole_card]
        
    # player has a blackjack if they're dealt 21
    player_blackjack = True if hand_value(player_hand) == 21 else False
    # the dealer peeks the hole card, and the dealer may also have a blackjack
    dealer_blackjack = True if hand_value(dealer_hand) == 21 else False
    
    # if both the player and the dealer have a blackjack, it's a push
    if player_blackjack and dealer_blackjack:
        return 0.0
    # if the player has a blackjack, they immediately win at 3:2
    if player_blackjack:
        return 1.5 * bet
    # if the dealer has a blackjack, they win (player loses the bet)
    if dealer_blackjack:
        return -bet        

    # play the player's hand according to player strategy
    play_hand(deck, player_hand, strategy, dealer_card)
    player_value = hand_value(player_hand)
    
    if player_value > 21:
        # player goes bust and loses immediately
        return -bet

    # play the dealer's hand according to dealer strategy
    play_hand(deck, dealer_hand, dealer_strategy, dealer_card)    
    dealer_value = hand_value(dealer_hand)

    if dealer_value > 21:
        # dealer goes bust and the player wins 1:1
        return bet

    # if neither busts, then the winner is the one with larger total
    if player_value == dealer_value:
        # equal values is a push
        return 0.0

    if player_value > dealer_value:
        # player wins 1:1
        return bet
    
    assert dealer_value > player_value
    # player loses the bet
    return -bet



def basic_strategy(hand: List[Card], dealer_card: Card)->Decision:
    dealer_value = dealer_card._rank.value
    if dealer_value > 10:
        dealer_value = 10
    elif dealer_value == 1:
        dealer_value = 11
    value = hand_value(hand)

    if len(hand) == 2 and \
      (hand[0]._rank == Rank.ACE or hand[1]._rank == Rank.ACE):
        # soft hand
        if value < 18:
            return Decision.HIT
        elif value == 18 and 9 <= dealer_value <= 10:
            return Decision.HIT
        else:
            return Decision.STAND
    elif 4 <= value <= 11:
        return Decision.HIT
    elif value == 12:
        if 4 <= dealer_value <= 6:
            return Decision.STAND
        else:
            return Decision.HIT
    elif 13 <= value <= 16:
        if 2 <= dealer_value <= 6:
            return Decision.STAND
        else:
            return Decision.HIT
    elif 17 <= value:
        return Decision.STAND
    else:
        assert False
    return Decision.STAND



def simulate(n: int,
                 strategy: strategy_type = basic_strategy,
                 num_workers: int = 1,
                 seed: Optional[int] = None)->float:
    """
    Simulate playing n deals of blackjack using a given strategy. 
    Return the expected wins/losses.

    Parameters:
    - n: number of deals to make
    - strategy: strategy to use for simulation
    - seed: optional random number seed to make the results reproducible
    """

    results: npt.NDArray[np.float64] = np.zeros(n)
    for i in range(n):
        results[i] = play_blackjack(basic_strategy)

    res: float = results.mean()
    return res


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'Blackjack',
        description = 'A very simple Blackjack strategy simulator',
        )
    parser.add_argument('n', type = int, 
                            help = 'The number of deals to simulate')

    # You must change the implementation for this argument to have an effect
    parser.add_argument('-w', '--workers', type = int, default = 1, metavar = 'W',
                            help = 'Number of workers (processes)')

    # You must change the implementation for this argument to have an effect
    parser.add_argument('--seed', type = int, required = False,
                            help = 'Random number seed to make the simulation '\
                            'reproducible')
    
    args = parser.parse_args()

    n = args.n
    num_workers = args.workers

    start = time.time() # starting timepoint
    res = simulate(n)
    end = time.time() # end timepoint
    print(f'{num_workers},{n},{res},{end-start}')
