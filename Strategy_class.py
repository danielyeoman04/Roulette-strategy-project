import scipy.special as sc
import numpy as np
from collections import deque
from Roulette_class import Roulette


class RollingOnesCounter:
    def __init__(self, max_size):
        self.max_size = max_size
        self.buffer = deque(maxlen=max_size)
        self.ones_count = 0

    def append(self, value):
        if len(self.buffer) == self.max_size:
            self.ones_count -= self.buffer.popleft()
        self.buffer.append(value)
        self.ones_count += value

    def count_ones(self):
        return self.ones_count
    
class Strategy:

    def __init__(self, purse = 1000, training_spins = 100, confidence_inteval = 0.85, max_bet_size = 2000, mult = 0.1, basket_scales = [300,50,20]):
        #Total remaining funds
        self.purse = purse
        #No. spins before starting to bet
        self.training_spins = training_spins
        #Confidence inteval value has to fall into to start betting
        self.confidence_inteval = confidence_inteval
        #Maximum bet size allowed
        self.max_bet_size = max_bet_size
        #Multiple of purse able to bet on a single spin
        self.mult = mult
        #List giving the consideration range for [single_numbers, thirds, halfs]
        self.basket_scales = basket_scales
        #Number of simulations passed
        self.sims = 0
        #Max value of funds attained (used for simulation purposes)
        self.max_value = purse
        #The baskets for each potential bet
        #!!!!Maybe make it so single bets are optional
        self.baskets = {
        '0' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '1' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '2': [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '3' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '4' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '5' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '6' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '7' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '8' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '9' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '10' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '11' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '12' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '13' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '14' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '15' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '16' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '17' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '18' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '19' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '20' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '21' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '22' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '23' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '24' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '25' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '26' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '27' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '28' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '29' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '30' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '31' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '32' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '33' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '34' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '35' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '36' : [RollingOnesCounter(self.basket_scales[0]), 1/37, 0],
        '1-12' : [RollingOnesCounter(self.basket_scales[1]), 12/37, 0],
        '13-24' : [RollingOnesCounter(self.basket_scales[1]), 12/37, 0],
        '25-36' : [RollingOnesCounter(self.basket_scales[1]), 12/37, 0],
        '1-34' : [RollingOnesCounter(self.basket_scales[1]), 12/37, 0],
        '2-35' : [RollingOnesCounter(self.basket_scales[1]), 12/37, 0],
        '3-36' : [RollingOnesCounter(self.basket_scales[1]), 12/37, 0],
        'black' : [RollingOnesCounter(self.basket_scales[2]), 18/37, 0],
        'red' : [RollingOnesCounter(self.basket_scales[2]), 18/37, 0],
        'odds' : [RollingOnesCounter(self.basket_scales[2]), 18/37, 0],
        'evens' : [RollingOnesCounter(self.basket_scales[2]), 18/37, 0],
        '1-18' : [RollingOnesCounter(self.basket_scales[2]), 18/37, 0],
        '19-36' : [RollingOnesCounter(self.basket_scales[2]), 18/37, 0]}



    def sim_single(self, prior_spin, p = False):
        '''
        Simulates a single spin in roulette.
        NOTE: does not handle the changing of the funds of self.purse
        Input: Prior spin
        Output:
        [0] - the list of proposed bet quantity pairs.
        [1] - the sum of the quantities of all the proposed bets.
        Optional Variables: p = True will print out the list of proposed bet quantity pairs.
        '''
        #Initialise and update parameters, require purse > 0 to continue
        if self.purse > 0:
            self.sims += 1
            hits = Roulette.hit_values(prior_spin)
            bets = []
            quantities = []

            # Update the list of total hits in last X spins for each bet
            for bet, counter in self.baskets.items():
                if bet in hits:
                    counter[0].append(1)
                else:
                    counter[0].append(0)

                #The integral representing the cumulative distribution function (Unregularized inverse beta)
                counter[2] = 1 - sc.betainc(len(counter[0].buffer) - counter[0].count_ones(), counter[0].count_ones() + 1, 1 - counter[1])

                #We want to halt the program from continuing to bet if we have not yet done enough 'training spins'
                if self.sims < self.training_spins:
                    continue

                #Get quantities for each bet
                quantity = self.bet_transform(counter[2])
                if quantity != 0:
                    bets.append(bet)
                    quantities.append(quantity)

            #scale the quantities down if they are greater than the max bet size or chosen criterion for percentage of purse
            if sum(quantities) > min(self.max_bet_size, self.mult*self.purse):
                quantities = self.scale(quantities)

            #compile bet and quantities into a single list
            bqs = [[bets[i], quantities[i]] for i, _ in enumerate(bets)]
            returned_bets = []
            #remove bets with quantity of 0
            for bq in bqs:
                if bq[1] >= 1:
                    returned_bets.append(bq)

            #Optional print statement
            if p == True:
                print(f'Made bets: {returned_bets}')

            return returned_bets, sum(quantities)


    def bet_transform(self, confidence_val):
        '''
        The currently used method of determining bet sizing
        NOTE: W.I.P. Strategy would be improved if this were entirely replaced with ML optimisation
        Input:
        - The CI for each possible bet
        - The key value of CI required before Strategy starts to bet
        Output:
        - The unscaled proposed quantity associated with the confidence inteval of the bet
        '''
        if confidence_val < self.confidence_inteval:
            return 0
        else:
            return np.floor((self.purse) ** ((confidence_val - self.confidence_inteval)/(1-self.confidence_inteval)))

    def scale(self, vals):
        '''
        Input: A list of the quantities associated with each bet
        Output: A list of quantities, all in the same proportion but scaled down to ensure bet does not exceed max_bet_size
        '''
        updated = []
        for val in vals:
            updated.append(np.floor(val * (min(self.mult * self.purse, self.max_bet_size)/sum(vals))))
        return updated

    def getbets(self, p = False):
        '''
        Input: Most recent spin
        Output: Recommeneded bet quantity pairs for next spin
        Optional Variables: p = True prints out the current CI for each bet
        '''
        strategy_bets, _ = self.sim_single(prior_spin = int(input('What was the spin?: ')))
        if p == True:
            for bet,counter in self.baskets.items():
                print(f'{bet}, CI = {counter[2]}')
        return strategy_bets