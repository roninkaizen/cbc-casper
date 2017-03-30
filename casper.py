'''
Casper PoC: Correct-by-construction asynchronous binary consensus.

Note that comments marked with "#########....#########"" barriers are probably
conceptually important Other comments may be conceptually important but are
mostly for code comprehension Note that not all comments have been marked up in
this manner, yet... :)
'''

import sys

import random as r  # to ensure the tie-breaking property

from settings import NUM_VALIDATORS, VALIDATOR_NAMES, WEIGHTS
from bet import Bet
from view import View
from adversary import Adversary
from network import Network



if sys.argv[1:] == ['rounds']:

    network = Network()

    print "WEIGHTS", WEIGHTS

    decided = dict.fromkeys(VALIDATOR_NAMES, 0)
    safe_bets = set()

    network.random_initialization()
    while(True):

        network.report(safe_bets)

        # for i in xrange(NUM_VALIDATORS):
        #    network.validators[i].view.plot_view(safe_bets)

        last_bets = []

        for i in xrange(NUM_VALIDATORS):
            last_bets.append(network.validators[i].my_latest_bet)

        for i in xrange(NUM_VALIDATORS):
            for j in xrange(NUM_VALIDATORS):
                if i != j and (r.randint(0, 4
                    ) == 0):
                    network.propagate_bet_to_validator(last_bets[j], i)

            if not decided[i]:
                new_bet = network.get_bet_from_validator(i)
                decided[i] = network.validators[i].decided

                if decided[i]:
                    safe_bets.add(new_bet)

elif sys.argv[1:] == ['blockchain']:
    
    network = Network()

    print "WEIGHTS", WEIGHTS

    decided = dict.fromkeys(VALIDATOR_NAMES, 0)
    safe_bets = set()

    random_bet = Bet(r.randint(0, 1), set(), 0)
    initial_view = View(set([random_bet]))
    network.view_initialization(initial_view)
    iterator = 0

    while(True):
        network.report(safe_bets)

        #for i in xrange(NUM_VALIDATORS):
        #    network.validators[i].view.plot_view(safe_bets)

        current_validator = iterator % NUM_VALIDATORS
        next_validator = (iterator + 1) % NUM_VALIDATORS

        bet = network.validators[current_validator].my_latest_bet

        if isinstance(bet, Bet):
            network.propagate_bet_to_validator(bet, next_validator)

        if not decided[next_validator]:
            new_bet = network.get_bet_from_validator(next_validator)
            decided[next_validator] = network.validators[next_validator].decided

            if decided[next_validator]:
                safe_bets.add(new_bet)

        iterator += 1
else:
    print "\nusage: 'kernprof -l casper.py rounds' or 'kernprof -l casper.py blockchain'\n"