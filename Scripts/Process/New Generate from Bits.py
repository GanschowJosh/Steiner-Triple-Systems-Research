import sys
import os
import graph as graph
from STSGenerator import isSteinerTripleSystem

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
    have_prev = False
    soln_size = 0
    prev_soln_size = 0
    orbs = {}
    orblens = {}
    soln = []
    counter = 0
    chunk = []

    for line in sys.stdin:
        line = line.strip()
        if counter < 100:
            print(line)
            counter += 1
        if line.startswith("$"):
            parts = line.split(maxsplit=1)
            key = int(parts[0][1:])  # remove the $ sign and convert to integer
            value = parts[1]
            
            if have_prev:
                prev_soln_size = 0
                orbs.clear()
                orblens.clear()
                have_prev = False
            
            orbs[key] = value
            orblens[key] = len(value.split())
            
        else:
            a = list(map(int, line.split()))
            total_len = 0
            
            # Calculate total length of orbits
            for x in a:
                if x not in orbs:
                    raise ValueError("Orbit not known")
                total_len += orblens[x]
            
            if have_prev:
                j = soln_size - 1
                while total_len > 0:
                    total_len -= orblens[soln[j]]
                    j -= 1
                j += 1
            else:
                j = 0
            
            soln_size = j + len(a)
            
            # Update solution array
            for i in range(len(a)):
                if len(soln) > j:
                    soln[j] = a[i]
                else:
                    soln.append(a[i])
                j += 1
            
            have_prev = True
            
            # Output matrix in usable form
            for i in range(soln_size):
                b = orbs[soln[i]].split()
                for item in b:
                    chunk.append(item)
                    if len(chunk) == 70:
                        systemFromBits(chunk)
                        chunk.clear() #resetting chunk for next group

    if chunk:
        systemFromBits(chunk)
    print(best)
    print(valid/(valid+invalid))