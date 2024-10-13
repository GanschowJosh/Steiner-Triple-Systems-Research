"""
Script to take input of lines of binary and construct system
"""

import sys
import Scripts.graph as graph
from STSGenerator import isSteinerTripleSystem
import os

best = []
valid = 0
invalid = 0

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
    