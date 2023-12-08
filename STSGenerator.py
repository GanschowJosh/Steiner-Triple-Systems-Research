import random
import hashlib
import json
from itertools import permutations
import time

# Get the order of the desired system from user input
v = int(input("Enter order of desired system:\t"))

# Adjust for 0-based indexing
LivePoints = [0] * (v+1)
IndexLivePoints = [0] * (v+1)
NumLivePairs = [0] * (v+1)
LivePairs = [[0]*(v+1) for _ in range(v+1)]
IndexLivePairs = [[0]*(v+1) for _ in range(v+1)]
Other = [[0]*(v+1) for _ in range(v+1)]

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

# Function to initialize the data structures
def initialize(v):
    global NumLivePoints
    global LivePoints, IndexLivePoints
    global NumLivePairs
    global LivePairs, Other

    NumLivePoints = v
    for x in range(1, v+1):  # Adjust the range
        LivePoints[x] = x
        IndexLivePoints[x] = x
        NumLivePairs[x] = v - 1
        for y in range(1, v):  # Adjust the range
            LivePairs[x][y] = ((y+x-1)%v)+1
        for y in range(1, v+1):  # Adjust the range
            IndexLivePairs[x][y] = (y-x)%v
            Other[x][y] = 0

# Function to insert a pair into the system
def InsertPair(x, y):
    global NumLivePoints
    global LivePoints, IndexLivePoints
    global NumLivePairs
    global LivePairs

    if NumLivePairs[x] == 0:
        NumLivePoints += 1
        LivePoints[NumLivePoints] = x
        IndexLivePoints[x] = NumLivePoints
    NumLivePairs[x] += 1
    posn = NumLivePairs[x]
    LivePairs[x][posn] = y
    IndexLivePairs[x][y] = posn

# Function to delete a pair from the system
def DeletePair(x, y):
    global NumLivePoints
    global LivePoints, IndexLivePoints
    global NumLivePairs
    global LivePairs

    posn = IndexLivePairs[x][y]
    num = NumLivePairs[x]
    z = LivePairs[x][num]
    LivePairs[x][posn] = z
    IndexLivePairs[x][z] = posn
    LivePairs[x][num] = 0
    IndexLivePairs[x][y] = 0
    NumLivePairs[x] -= 1
    if NumLivePairs[x] == 0:
        posn = IndexLivePoints[x]
        z = LivePoints[NumLivePoints]
        LivePoints[posn] = z
        IndexLivePoints[z] = posn
        LivePoints[NumLivePoints] = 0
        NumLivePoints -= 1  # This line should be inside the if statement

# Function to add a block to the system
def AddBlock(x, y, z):
    global Other
    Other[x][y] = z
    Other[y][x] = z
    Other[x][z] = y
    Other[z][x] = y
    Other[y][z] = x
    Other[z][y] = x
    DeletePair(x,y)
    DeletePair(y,x)
    DeletePair(x,z)
    DeletePair(z,x)
    DeletePair(y,z)
    DeletePair(z,y)

# Function to exchange blocks in the system
def ExchangeBlock(x, y, z, w):
    global Other
    Other[x][y] = z
    Other[y][x] = z
    Other[x][z] = y
    Other[z][x] = y
    Other[y][z] = x
    Other[z][y] = x
    Other[w][y] = 0
    Other[y][w] = 0
    Other[w][z] = 0
    Other[z][w] = 0
    InsertPair(w, y)
    InsertPair(y, w)
    InsertPair(w, z)
    InsertPair(z, w)
    DeletePair(x, y)
    DeletePair(y, x)
    DeletePair(x, z)
    DeletePair(z, x)

# Function to perform a revised switch operation
def RevisedSwitch():
    global NumLivePoints
    global LivePoints, NumLivePairs
    global LivePairs, Other
    global NumBlocks

    r = random.randint(1, NumLivePoints)
    x = LivePoints[r]
    s, t = sorted(random.sample(range(1, NumLivePairs[x]+1), 2))
    y = LivePairs[x][s]
    z = LivePairs[x][t]
    if Other[y][z] == 0:
        AddBlock(x,y,z)
        NumBlocks += 1
    else:
        w = Other[y][z]
        ExchangeBlock(x, y, z, w)

# Function to construct blocks from the system
def ConstructBlocks(v, Other):
    B = []
    for x in range(1, v):
        for y in range(x+1, v):
            z = Other[x][y]
            if z > y:
                B.append({x, y, z})
    return B

def canonicalForm(S, T):
    startTime = time.time()
    # Generate all permutations of S
    perms = permutations(S)
    
    # Initialize the canonical form to be the lexicographically first triple system
    canonicalT = sorted(sorted(triple) for triple in T)
    
    for perm in perms:
        # Create a mapping from the original points to the permuted points
        alpha = {S[i]: perm[i] for i in range(len(S))}
        
        # Apply the permutation to T
        tPerm = [{alpha[point] for point in triple} for triple in T]
        tPerm = sorted(sorted(triple) for triple in tPerm)

        
        # Update the canonical form if necessary
        if tPerm < canonicalT:
            canonicalT = tPerm
    
    print(f"Time taken to find canonical form: {time.time() - startTime:.5f} seconds")

    return canonicalT

def generateKey(S, T):
    # Generate the canonical form of the STS
    canonicalT = canonicalForm(S, T)
    
    # Serialize the canonical form
    serializedT = json.dumps(canonicalT).encode('utf-8')
    
    # Generate a SHA-256 hash of the serialized canonical form
    hashObject = hashlib.sha256(serializedT)
    return hashObject.hexdigest()

# Function to implement Revised Stinson's Algorithm
def RevisedStinsonsAlgorithm(v):
    global NumBlocks, Other

    NumBlocks = 0
    initialize(v)
    while NumBlocks < v*(v-1)/6:
        RevisedSwitch()
    B = ConstructBlocks(v, Other)
    print(B)
    '''S = set()
    for triple in B:
        S.update(triple)
    S = list(S)
    key = generateKey(S, B)
    print(key)'''
    print(isSteinerTripleSystem([n+1 for n in range(v)], B))

# Check if the order is valid for a Steiner triple system
if v % 6 not in [1,3]:
    print(f"{v} is not a valid order for a Steiner triple system")
else:
    RevisedStinsonsAlgorithm(v)
