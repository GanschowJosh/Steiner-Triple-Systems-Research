"""
Script to take input of lines of binary and construct system
"""

import sys
import Scripts.graph as graph
import os

best = []
valid = 0
invalid = 0
# Define a function to check if a set of points and triples is a Steiner triple system
def isSteinerTripleSystem(points, triples):
    # Create a set of all triples
    triples_set = set(map(frozenset, triples))

    # Check if every pair of points appears in exactly one triple
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pair = frozenset([points[i], points[j]])
            count = sum(1 for triple in triples_set if pair.issubset(triple))
            if count != 1:
                return False

    # Check that each triple has exactly 3 points
    if any(len(triple) != 3 for triple in triples_set):
        return False

    # Check if the order of the system is congruent to 1 or 3 modulo 6
    order = len(points)
    if order % 6 not in [1, 3]:
        return False

    # Return True if all checks passed
    return True

def printProgressBar(iteration, total, length=50):
    progress = int(length*iteration//total)
    bar = '█' * progress + '-' * (length - progress)
    percent = (iteration/total)*100
    os.system('cls')
    print(f"\r|{bar}| {percent:.2f}% complete")

def systemFromBits(bits):
    global valid, invalid
    if not (valid+invalid)%100:
        printProgressBar(valid+invalid, 65000000)
        print(valid+invalid)
    currSystem = []
    for line in bits:
        currBlock = []
        for char in range(len(line)):
            if line[char] == "1":
                currBlock.append(char+1)
        currSystem.append(set(currBlock))
    if isSteinerTripleSystem(list(i+1 for i in range(21)), currSystem):
        #print(currSystem)
        valid += 1
        maxCycle = graph.processSystem(currSystem)
        if maxCycle < 18:
            best.append(currSystem)
            with open("out.txt", "a") as file:
                file.write(f"{currSystem}\n")
            print(currSystem)
            
    else:
        print("ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
        invalid += 1
    #print(valid/(invalid+1))
    
    """try:
        print(valid/invalid)
    except:
        return"""

"""numLines = 70
while True:
    currSystem = []
    for i in range(numLines):
        inputString = input()
        currBlock = []
        for char in range(len(inputString)):
            if inputString[char] == "1":
                currBlock.append(char+1)
                #print("here")
        
        currSystem.append(set(currBlock))
    print(isSteinerTripleSystem(list(i+1 for i in range(21)), currSystem))"""

""" Testing
li = ['100110000000000000000', '010011000000000000000', '001101000000000000000', '100001100000000000000', '010100010000000000000', '001010001000000000000', '100000000110000000000', '010000000011000000000', '001000000101000000000', '100000010001000000000', '010000001100000000000', '001000100010000000000', '100000001000100000000', '010000100000010000000', '001000010000001000000', '100000000000010100000', '010000000000001010000', '001000000000100001000', '100000000000001001000', '010000000000100100000', '001000000000010010000', '100000000000000010100', '010000000000000001010', '001000000000000100001', '110000000000000000001', '011000000000000000100', '101000000000000000010', '000100100100000000000', '000010010010000000000', '000001001001000000000', '000100000000100000001', '000010000000010000100', '000001000000001000010', '000100000000011000000', '000010000000101000000', '000001000000110000000', '000000000100001100000', '000000000010100010000', '000000000001010001000', '000000100001001000000', '000000010100100000000', '000000001010010000000', '000000100000100000100', '000000010000010000010', '000000001000001000001', '000000000100010000001', '000000000010001000100', '000000000001100000010', '000100000010000001000', '000010000001000100000', '000001000100000010000', '000100000001000010000', '000010000100000001000', '000001000010000100000', '000000000100000000110', '000000000010000000011', '000000000001000000101', '000100000000000100100', '000010000000000010010', '000001000000000001001', '000100001000000000010', '000010100000000000001', '000001010000000000100', '000000100000000100010', '000000010000000010001', '000000001000000001100', '000000110000000001000', '000000011000000100000', '000000101000000010000', '000000000000000111000']
sys = systemFromBits(li)
print(sys)
print(isSteinerTripleSystem(list(i+1 for i in range(21)), sys))
"""

if __name__ == "__main__":
    chunk = []
    for line in sys.stdin:
        if line.strip(): #ignoring empty
            chunk.append(line.strip())
        
        if len(chunk) == 70:
            systemFromBits(chunk)
            chunk = [] #resetting chunk for next group
    
    if chunk:
        systemFromBits(chunk)
    print(best)
    print(valid/(valid+invalid))
    
    
#print(isSteinerTripleSystem(list(i+1 for i in range(21)), [{16, 2, 13}, {17, 3, 14}, {1, 19, 17}, {2, 18, 20}, {16, 3, 21}, {1, 2, 21}, {19, 2, 3}, {1, 3, 20}, {10, 4, 14}, {11, 5, 15}, {12, 13, 6}, {4, 13, 7}, {8, 5, 14}, {9, 6, 15}, {19, 4, 15}, {13, 20, 5}, {21, 6, 14}, {13, 14, 15}, {17, 10, 13}, {18, 11, 14}, {16, 12, 15}, {15, 21, 7}, {8, 19, 13}, {9, 20, 14}, {10, 20, 15}, {21, 11, 13}, {19, 12, 14}, {17, 11, 4}, {18, 12, 5}, {16, 10, 6}, {9, 4, 12}, {10, 5, 7}, {8, 11, 6}, {16, 18, 4}, {16, 17, 5}, {17, 18, 6}, {21, 4, 20}, {21, 19, 5}, {19, 20, 6}, {19, 10, 18}, {16, 11, 20}, {17, 12, 21}, {12, 20, 7}, {8, 10, 21}, {19, 9, 11}, {16, 19, 7}, {8, 17, 20}, {9, 18, 21}, {8, 18, 7}, {8, 9, 16}, {9, 17, 7}, {1, 4, 5}, {2, 5, 6}, {3, 4, 6}, {1, 6, 7}, {8, 2, 4}, {9, 3, 5}, {1, 10, 11}, {2, 11, 12}, {10, 3, 12}, {8, 1, 12}, {9, 2, 10}, {11, 3, 7}, {1, 13, 9}, {2, 14, 7}, {8, 3, 15}, {16, 1, 14}, {17, 2, 15}, {18, 3, 13}]))      