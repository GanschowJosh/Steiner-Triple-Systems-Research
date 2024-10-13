import graph as graph 
from STSGenerator import generateSteinerTripleSystem, isSteinerTripleSystem
import csv
import sys

# Function to write the results to a CSV file
def write_to_csv(system, pairDict, total_max_cycle, fileNumber, directory):
    try:
        outputFilename = f'{directory}/output{fileNumber}.csv'
        with open(outputFilename, 'a', newline='') as csvfile:
            fieldnames = ['System', 'Max Cycle Pair', 'Total Max Cycle']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'System': str(system), 'Max Cycle Pair': str(pairDict), 'Total Max Cycle': str(total_max_cycle)})
    except Exception as e:
        print(f"Exception occurred: {e}")
        sys.exit()


def externalwriting(directory, v):
    counter = 1
    fileNumber = 0
    print("Working on file #1")
    while True:
        try:
            steinerSystem = generateSteinerTripleSystem(v)
        except:
            return
        pairs = []
        pairDict = {}
        maxCycle = 0
        for a in range(v, 0, -1):
            for b in range(1, v+1):
                if a!=b:
                    pairs.append((a, b))
        for pair in pairs:
            a, b = pair
            ret = graph.cycleFromPair(a, b, steinerSystem)
            if ret > maxCycle:
                maxCycle = ret
            pairDict[(a,b)] = ret
        if maxCycle < v-3:
            print(steinerSystem)
            break
        write_to_csv(steinerSystem, pairDict, maxCycle, fileNumber + 1, directory)
        if counter % 10000 == 0:
            print(f"Working on file #{fileNumber + 2}")
            fileNumber += 1

if __name__ == "__main__":
    directoryPath = input("What directory would you like your output files in (forward slash separators please)? ")
    externalwriting(directoryPath, int(input("What order of systems would you like to generate? ")))