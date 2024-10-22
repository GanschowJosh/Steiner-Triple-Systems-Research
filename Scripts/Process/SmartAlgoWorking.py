import random
import Scripts.graph as graph 
import csv

# Get the order of the desired system from user input
v = int(input("Enter order of desired system:\t"))

# Adjust for 0-based indexing
LivePoints = [0] * (v+1)
IndexLivePoints = [0] * (v+1)
NumLivePairs = [0] * (v+1)
LivePairs = [[0]*(v+1) for _ in range(v+1)]
IndexLivePairs = [[0]*(v+1) for _ in range(v+1)]
Other = [[0]*(v+1) for _ in range(v+1)]
maxCycleThreshold = 12
currentSystem = None 

def scoreSystem(system):
    circum = []
    pairs = [(a,b) for a in range(v, 0, -1) for b in range(1, v+1) if a != b]
    for pair in pairs:
        a, b = pair
        print(system)
        ret = graph.cycleFromPair(a, b, system)
        circum.append(ret)
    return max(circum)

def findBestTriple(currentSystem):
    if currentSystem is None:
        return None
    bestScore = float('inf')
    bestTriple = None
    for x in range(1, v+1):
        for y in range(x+1, v+1):
            for z in range(y+1, v+1):
                #temporarily add the triple to the system
                AddBlock(x, y, z)
                currentScore = scoreSystem(currentSystem)
                
                #if the current score is better, update the bets score
                if currentScore < bestScore:
                    bestScore = currentScore
                    bestTriple = (x, y, z)
                
                #revert the changes for the next iteration
                DeletePair(x, y)
                DeletePair(y, z)
                DeletePair(x, z)
    print("Best triple: ", bestTriple, "Best Score: ", bestScore)
    return bestTriple 

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
        NumLivePoints -= 1  

# Function to add a block to the system
def AddBlock(x, y, z, currentSystem):
    global Other
    Other[x][y] = z
    Other[y][x] = z
    Other[x][z] = y
    Other[z][x] = y
    Other[y][z] = x
    Other[z][y] = x
    currentSystem = ConstructBlocks(v, Other)
    if currentSystem is not None:
        DeletePair(x,y)
        DeletePair(y,x)
        DeletePair(x,z)
        DeletePair(z,x)
        DeletePair(y,z)
        DeletePair(z,y)
    return currentSystem
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
def RevisedSwitch(currentSystem):
    global NumLivePoints
    global LivePoints, NumLivePairs
    global LivePairs, Other
    global NumBlocks

    r = random.randint(1, NumLivePoints)
    x = LivePoints[r]
    s, t = sorted(random.sample(range(1, NumLivePairs[x]+1), 2))
    y = LivePairs[x][s]
    z = LivePairs[x][t]

    #backup the state of other
    backupOther = [row[:] for row in Other]

    #temporarily add the triple to the system
    AddBlock(x, y, z)
    print(currentSystem)
    currentScore = scoreSystem(currentSystem)

    if currentScore < maxCycleThreshold:
        NumBlocks += 1
        #the switch is accepted, no need to revert the changes
    else:
        Other = backupOther


# Function to construct blocks from the system
def ConstructBlocks(v, Other):
    global currentSystem
    B = []
    for x in range(1, v):
        for y in range(x+1, v):
            z = Other[x][y]
            if z > y:
                B.append({x, y, z})
    currentSystem = list(B)
    print(currentSystem)
    return currentSystem

#smart hill climbing algorithm
def SmartHillClimbing():
    global NumBlocks, Other
    NumBlocks = 0
    currentSystem = initialize(v)
    while NumBlocks < v * (v-1) / 6:
        bestTriple = findBestTriple(currentSystem)
        currentSystem = RevisedSwitch(currentSystem)
        currentSystem = AddBlock(*bestTriple, currentSystem)
    currentSystem = ConstructBlocks(v, Other)
    #print(currentSystem)
    if currentSystem is not None:
        score = scoreSystem(currentSystem)
        return currentSystem, score 
    else:
        return None, None
    

# Function to implement Revised Stinson's Algorithm
def RevisedStinsonsAlgorithm(v):
    global NumBlocks, Other

    NumBlocks = 0
    initialize(v)
    while NumBlocks < v*(v-1)/6:
        RevisedSwitch()
    B = ConstructBlocks(v, Other)
    #print(B)
    return B
    
# Function to write the results to a CSV file
def write_to_csv(system, pairDict, total_max_cycle, fileNumber):
    #print(fileNumber)
    outputFilename = f'./CycleGeneration/output{fileNumber}.csv'
    with open(outputFilename, 'a', newline='') as csvfile:
        fieldnames = ['System', 'Max Cycle Pair', 'Total Max Cycle']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'System': str(system), 'Max Cycle Pair': str(pairDict), 'Total Max Cycle': str(total_max_cycle)})

def externalwriting():
    counter = 0
    fileNumber = 0
    while(True):
        steinerSystem = RevisedStinsonsAlgorithm(v)
        
        pairs = []
        pairDict = {}
        circum = []
        for a in range(25, 0, -1):
            for b in range(1, 26):
                if a!=b:
                    pairs.append((a, b))
        #print(pairs)
        for pair in pairs:
            a, b = pair
            ret = graph.cycleFromPair(a, b, steinerSystem)
            circum.append(ret)
            pairDict[(a,b)] = ret
        maxCycle = max(circum)
        if max(circum) < 12:
            print(steinerSystem)
            break
        write_to_csv(steinerSystem, pairDict, maxCycle, fileNumber + 1)
        counter+=1
        if counter % 10000 == 0:
            print(f"Working on file #{fileNumber + 2}")
            fileNumber += 1

if v % 6 not in [1,3]:
    print(f"{v} is not a valid order for a Steiner Triple System")
else:
    smartSystem, smartScore = SmartHillClimbing()
    if smartSystem is not None:
        print(smartSystem, smartScore)
    else:
        print("Not done")
    #externalwriting()

'''
# Check if the order is valid for a Steiner triple system
if v % 6 not in [1, 3]:
    print(f"{v} is not a valid order for a Steiner triple system")
else:
    counter = 0
    fileNumber = 0
    while(True):
        steinerSystem = RevisedStinsonsAlgorithm(v)
        
        pairs = []
        pairDict = {}
        circum = []
        for a in range(25, 0, -1):
            for b in range(1, 26):
                if a!=b:
                    pairs.append((a, b))
        #print(pairs)
        for pair in pairs:
            a, b = pair
            ret = graph.cycleFromPair(a, b, steinerSystem)
            circum.append(ret)
            pairDict[(a,b)] = ret
        maxCycle = max(circum)
        if max(circum) < 12:
            print(steinerSystem)
            break
        write_to_csv(steinerSystem, pairDict, maxCycle, fileNumber + 1)
        counter+=1
        if counter % 10000 == 0:
            print(f"Working on file #{fileNumber + 2}")
            fileNumber += 1
'''