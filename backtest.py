from Strategy_class import Strategy
from Dylan_strategy_class import Dylan_strategy
from Roulette_class import Roulette
import random
import copy
import numpy as np
from tabulate import tabulate

def backtest(strategy, cutoff_spins = 1000, runs = 1000, key_value_parameters = {}, funds = 1000, p = False):
    '''
    Function which tests the chosen strategy.
    Input:
    - Strategy
    Output:
    - 3 Tables, giving the Min, 5th, 25th, Median, 75th, 95th and Max Quartiles for sims, max and terminal value
    Optional Variables:
    cutoff_spins: no. of spins before exiting the simulation, useful for strategy which can otherwise require lots of time to run
    runs: the number of runs to do
    key_value_parameters: a dictionary containing optional values to overwrite in the chosen strategy:
    For Dylan_strategy these optional paramaters are:
    - purse
    -initial_bet
    For Strategy they are:
    - purse
    - confidence_inteval
    - mult
    -basket_scales (list of 3, [0] for single spins, [1] for thirds and [2] for halves)
    -training_spins
    -max_bet_size
    '''

    #Initialise lists which store total sims before bust and terminal/maximal value
    sim_list = []
    terminal_value_list = []
    max_value_list = []

    for _ in range(runs):
        strat = strategy(**key_value_parameters) #Unpacks any updates to the parameters if specified
        strat.funds = funds
        if strategy == Strategy:
            key_cutoff = 1/strat.mult  #required as Strategy is only able to bet at most mult*purse per bet, so once it falls below this value it will continue to run with no bets
            sim = 1-(strat.training_spins)
        else:
            key_cutoff = 0
            sim  = 0
        prior_spin = random.randint(0,36)
        while sim < cutoff_spins:
            if strat.purse > key_cutoff:
                sim  += 1
                spin = random.randint(0,36)
                bets, squantities = strat.sim_single(prior_spin = prior_spin)
                prior_funds_temp = strat.purse
                returns = Roulette(bets, spin = spin).returns()
                strat.purse += returns - squantities
                prior_spin = copy.copy(spin)
                strat.max_value  = max(strat.max_value, strat.purse)


                if p == True:
                    print(f'Spin was {spin}, sim = {sim}')
                    print(f'Bets were {bets}')
                    print(f'Returned {strat.purse - prior_funds_temp}, total value of bets was {squantities}')

                    #if strategy == Strategy:
                    #    for bet,counter in strat.baskets.items():
                    #        print(f'{bet}, CI = {counter[2]}')
                    print(f'Current funds are {strat.purse}')


            else:
                break



        terminal_value_list.append(strat.purse)
        sim_list.append(sim)
        max_value_list.append(strat.max_value)
    if p == True:
        print(sim_list)
        print(terminal_value_list)
        print(max_value_list)


        #Assign data to print in table
    headers = ['Quantile', 'Value']
    sim_data = [['Min', min(sim_list)],
                ['5',np.quantile(sim_list, 0.05)],
                ['25',np.quantile(sim_list,0.25)],
                ['Median', np.quantile(sim_list, 0.5)],
                ['75', np.quantile(sim_list, 0.75)],
                ['95', np.quantile(sim_list, 0.95)],
                ['Max', max(sim_list)]]
    terminal_value_data =    [['Min', min(terminal_value_list)],
                    ['5',np.quantile(terminal_value_list, 0.05)],
                    ['25',np.quantile(terminal_value_list,0.25)],
                    ['Median', np.quantile(terminal_value_list, 0.5)],
                    ['75', np.quantile(terminal_value_list, 0.75)],
                    ['95', np.quantile(terminal_value_list, 0.95)],
                    ['Max', max(terminal_value_list)]]
    max_value_data =    [['Min', min(max_value_list)],
                    ['5',np.quantile(max_value_list, 0.05)],
                    ['25',np.quantile(max_value_list,0.25)],
                    ['Median', np.quantile(max_value_list, 0.5)],
                    ['75', np.quantile(max_value_list, 0.75)],
                    ['95', np.quantile(max_value_list, 0.95)],
                    ['Max', max(max_value_list)]]



    return f'Spin analysis:\n {tabulate(sim_data, headers = headers)} \nTerminal value analysis:\n {tabulate(terminal_value_data, headers= headers)}\nMax value analysis:\n {tabulate(max_value_data, headers= headers)}'
