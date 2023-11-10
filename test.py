import random
v = 9
# Adjust for 0-based indexing
LivePoints = [0] * (v+1)
IndexLivePoints = [0] * (v+1)
NumLivePairs = [0] * (v+1)
LivePairs = [[0]*(v+1) for _ in range(v+1)]
IndexLivePairs = [[0]*(v+1) for _ in range(v+1)]
Other = [[0]*(v+1) for _ in range(v+1)]


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

def ConstructBlocks(v, Other):
    B = []
    for x in range(1, v):
        for y in range(x+1, v):
            z = Other[x][y]
            if z > y:
                B.append({x, y, z})
    return B

def RevisedStinsonsAlgorithm(v):
    global NumBlocks, Other

    NumBlocks = 0
    initialize(v)
    while NumBlocks < v*(v-1)/6:
        RevisedSwitch()
    B = ConstructBlocks(v, Other)
    print(B)

RevisedStinsonsAlgorithm(v)