'''
this file will serve for writing the methods that encode according with an alphabet
'''

class Encoding:
    '''
    alphabet - a matrix of DS having the corresponding 'symbol' on each position
    '''
    def __init__(self, alphabet):
        self.alphabet = []
        self.rows = 0
        self.cols = 0

    '''
    method to initialize the alphabet based on values read from a given file
    symbols_file - full path, name of the file
    rows and cols - the dim of the alphabet
    '''
    def read_alphabet(self, symbols_file, rows, cols):
        self.cols = cols
        self.rows = rows
        f = open(symbols_file, 'r')
        self.alphabet = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            for j in range(cols):
                f.read(self.alphabet[i][j])

    def get_symbol(self, d, s):
        if d < len(self.alphabet) and s < len(self.alphabet[0]):
         return self.alphabet[d][s]


