"""
This module houses all the functions for the generation of the Steiner Triple Systems
"""
import random

class SteinerTripleSystem:
    def __init__(self, v):
        self.v = v
        self.LivePoints = [0] * (v+1)
        self.IndexLivePoints = [0] * (v+1)
        self.NumLivePairs = [0] * (v+1)
        self.LivePairs = [[0]*(v+1) for _ in range(v+1)]
        self.IndexLivePairs = [[0]*(v+1) for _ in range(v+1)]
        self.Other = [[0]*(v+1) for _ in range(v+1)]
        self.NumLivePoints = v
        self.NumBlocks = 0

    # Function to initialize the data structures
    def initialize(self):
        NumLivePoints = self.v
        for x in range(1, self.v+1):  # Adjust the range
            self.LivePoints[x] = x
            self.IndexLivePoints[x] = x
            self.NumLivePairs[x] = self.v - 1
            for y in range(1, self.v):  # Adjust the range
                self.LivePairs[x][y] = ((y+x-1)%self.v)+1
            for y in range(1, self.v+1):  # Adjust the range
                self.IndexLivePairs[x][y] = (y-x)%self.v
                self.Other[x][y] = 0
    # Function to insert a pair into the system
    def InsertPair(self, x, y):
        if self.NumLivePairs[x] == 0:
            self.NumLivePoints += 1
            self.LivePoints[self.NumLivePoints] = x
            self.IndexLivePoints[x] = self.NumLivePoints
        self.NumLivePairs[x] += 1
        posn = self.NumLivePairs[x]
        self.LivePairs[x][posn] = y
        self.IndexLivePairs[x][y] = posn
    
    # Function to delete a pair from the system
    def DeletePair(self, x, y):
        posn = self.IndexLivePairs[x][y]
        num = self.NumLivePairs[x]
        z = self.LivePairs[x][num]
        self.LivePairs[x][posn] = z
        self.IndexLivePairs[x][z] = posn
        self.LivePairs[x][num] = 0
        self.IndexLivePairs[x][y] = 0
        self.NumLivePairs[x] -= 1
        if self.NumLivePairs[x] == 0:
            posn = self.IndexLivePoints[x]
            z = self.LivePoints[self.NumLivePoints]
            self.LivePoints[posn] = z
            self.IndexLivePoints[z] = posn
            self.LivePoints[self.NumLivePoints] = 0
            self.NumLivePoints -= 1 

    # Function to add a block to the system
    def AddBlock(self, x, y, z):
        self.Other[x][y] = z
        self.Other[y][x] = z
        self.Other[x][z] = y
        self.Other[z][x] = y
        self.Other[y][z] = x
        self.Other[z][y] = x
        self.DeletePair(x,y)
        self.DeletePair(y,x)
        self.DeletePair(x,z)
        self.DeletePair(z,x)
        self.DeletePair(y,z)
        self.DeletePair(z,y)

    # Function to exchange blocks in the system
    def ExchangeBlock(self, x, y, z, w):
        self.Other[x][y] = z
        self.Other[y][x] = z
        self.Other[x][z] = y
        self.Other[z][x] = y
        self.Other[y][z] = x
        self.Other[z][y] = x
        self.Other[w][y] = 0
        self.Other[y][w] = 0
        self.Other[w][z] = 0
        self.Other[z][w] = 0
        self.InsertPair(w, y)
        self.InsertPair(y, w)
        self.InsertPair(w, z)
        self.InsertPair(z, w)
        self.DeletePair(x, y)
        self.DeletePair(y, x)
        self.DeletePair(x, z)
        self.DeletePair(z, x)

    # Function to perform a revised switch operation
    def RevisedSwitch(self):
        r = random.randint(1, self.NumLivePoints)
        x = self.LivePoints[r]
        s, t = sorted(random.sample(range(1, self.NumLivePairs[x]+1), 2))
        y = self.LivePairs[x][s]
        z = self.LivePairs[x][t]
        if self.Other[y][z] == 0:
            self.AddBlock(x,y,z)
            self.NumBlocks += 1
        else:
            w = self.Other[y][z]
            self.ExchangeBlock(x, y, z, w)

    # Function to construct blocks from the system
    def ConstructBlocks(self):
        B = []
        for x in range(1, self.v):
            for y in range(x+1, self.v):
                z = self.Other[x][y]
                if z > y:
                    B.append({x, y, z})
        return B

    # Function to implement Revised Stinson's Algorithm
    def RevisedStinsonsAlgorithm(self):
        self.NumBlocks = 0
        self.initialize()
        while self.NumBlocks < self.v*(self.v-1)/6:
            self.RevisedSwitch()
        return self.ConstructBlocks()

#checks if a given v is valid for an order of a Steiner Triple System
def isValidOrder(v):
    return v%6 in [1, 3]

def generateSteinerTripleSystem(v):
    if not isValidOrder(v):
        raise ValueError(f"{v} is not a valid order for a Steiner Triple System")
    sts = SteinerTripleSystem(v)
    return sts.RevisedStinsonsAlgorithm()

# Define a function to check if a set of points and triples is a Steiner triple system
def isSteinerTripleSystem(points, triples):
    # Create a set of all triples
    triples_set = set(map(frozenset, triples))

    # Check if every pair of points appears in exactly one triple
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pair = frozenset([points[i], points[j]])
            count = sum(1 for triple in triples_set if pair <= triple)
            if count != 1:
                return False

    # Check if the order of the system is congruent to 1 or 3 modulo 6
    order = len(points)
    if order % 6 not in [1, 3]:
        return False

    # Return True if all checks passed
    return True

if __name__ == "__main__":
    v = int(input())
    try:
        result = generateSteinerTripleSystem(v)
        print(result)
    except ValueError as e:
        print(e)