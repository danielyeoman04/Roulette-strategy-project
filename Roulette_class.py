#Class which simulates a roulette wheel and calculates returns based on bets placed

class Roulette:
    validsingles = [str(i) for i in range(0,37)]
    validthirds = ['1-12', '13-24', '25-36', '1-34', '2-35', '3-36']
    validhalfs = ['1-18', '19-36', 'odds', 'evens', 'black', 'red']
    valid_bets = validsingles + validthirds + validhalfs

    def __init__(self, betquantities, spin):
        self.spin = int(spin)
        self.betquantities = betquantities

    @classmethod
    def hit_values(cls, spin):
        categories = {
                0: ['0'],
                1: ['1', 'red', 'odds', '1-18', '1-12', '1-34'],
                2: ['2', 'black', 'evens', '1-18', '1-12', '2-35'],
                3: ['3', 'red', 'odds', '1-18', '1-12', '3-36'],
                4: ['4', 'black', 'evens', '1-18', '1-12', '1-34'],
                5: ['5', 'red', 'odds', '1-18', '1-12', '2-35'],
                6: ['6', 'black', 'evens', '1-18', '1-12', '3-36'],
                7: ['7', 'red', 'odds', '1-18', '1-12', '1-34'],
                8: ['8', 'black', 'evens', '1-18', '1-12', '2-35'],
                9: ['9', 'red', 'odds', '1-18', '1-12', '3-36'],
                10: ['10', 'black', 'evens', '1-18', '1-12', '1-34'],
                11: ['11', 'black', 'odds', '1-18', '1-12', '2-35'],
                12: ['12', 'red', 'evens', '1-18', '1-12', '3-36'],
                13: ['13', 'black', 'odds', '1-18', '13-24', '1-34'],
                14: ['14', 'red', 'evens', '1-18', '13-24', '2-35'],
                15: ['15', 'black', 'odds', '1-18', '13-24', '3-36'],
                16: ['16', 'red', 'evens', '1-18', '13-24', '1-34'],
                17: ['17', 'black', 'odds', '1-18', '13-24', '2-35'],
                18: ['18', 'red', 'evens', '1-18', '13-24', '3-36'],
                19: ['19', 'red', 'odds', '19-36', '13-24', '1-34'],
                20: ['20', 'black', 'evens', '19-36', '13-24', '2-35'],
                21: ['21', 'red', 'odds', '19-36', '13-24', '3-36'],
                22: ['22', 'black', 'evens', '19-36', '13-24', '1-34'],
                23: ['23', 'red', 'odds', '19-36', '13-24', '2-35'],
                24: ['24', 'black', 'evens', '19-36', '13-24', '3-36'],
                25: ['25', 'red', 'odds', '19-36', '25-36', '1-34'],
                26: ['26', 'black', 'evens', '19-36', '25-36', '2-35'],
                27: ['27', 'red', 'odds', '19-36', '25-36', '3-36'],
                28: ['28', 'black', 'evens', '19-36', '25-36', '1-34'],
                29: ['29', 'black', 'odds', '19-36', '25-36', '2-35'],
                30: ['30', 'red', 'evens', '19-36', '25-36', '3-36'],
                31: ['31', 'black', 'odds', '19-36', '25-36', '1-34'],
                32: ['32', 'red', 'evens', '19-36', '25-36', '2-35'],
                33: ['33', 'black', 'odds', '19-36', '25-36', '3-36'],
                34: ['34', 'red', 'evens', '19-36', '25-36', '1-34'],
                35: ['35', 'black', 'odds', '19-36', '25-36', '2-35'],
                36: ['36', 'red', 'evens', '19-36', '25-36', '3-36']}

        return categories[spin]

    def returns(self):
        to_return = 0
        for value in self.betquantities:
            bet, quantity = value
            if bet in self.hit_values(self.spin):
                if bet in self.validsingles:
                    to_return += 36*quantity
                elif bet in self.validthirds:
                    to_return += 3*quantity
                else:
                    to_return += 2*quantity

        return to_return

    def __str__(self):
       return f'Bets:{self.betquantities}, spin was {self.spin}, returned {self.returns()}'