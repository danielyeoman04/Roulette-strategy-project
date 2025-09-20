from Roulette_class import Roulette

class Dylan_strategy:

    bets = ['1-12', '13-24', '25-36']


    def __init__(self, purse =1000, initial_bet =4):
        self.purse = purse
        self.initial_bet = initial_bet
        self.bet = '1-12'
        self.sims = 0
        self.prior_quantity = 0
        self.current_quantity = initial_bet
        self.max_value = purse

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
        if self.purse > 0:
            if self.sims == 0:
                self.sims += 1
                return [[self.bet, self.initial_bet]], self.initial_bet
            else:
                self.sims += 1
                hits = Roulette.hit_values(prior_spin)
                if self.bet in hits:
                    self.bet = self.bets[(self.bets.index(self.bet)+1)%3] # gets the next bet from the bets list
                    self.prior_quantity = 0
                    self.current_quantity = self.initial_bet
                else:
                    self.prior_quantity, self.current_quantity = self.current_quantity, min(self.purse, self.prior_quantity + self.current_quantity)

            return [[self.bet, self.current_quantity]], self.current_quantity


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
