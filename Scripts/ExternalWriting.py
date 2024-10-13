import Scripts.graph as graph 
import csv
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



def externalwriting(steinerSystem):
    counter = 0
    fileNumber = 0
    while(True):
        
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