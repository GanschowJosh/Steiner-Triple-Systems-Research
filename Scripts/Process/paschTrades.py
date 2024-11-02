import itertools
import Scripts.graph as graph
import Scripts.STSGenerator as STSGenerator
import time

v = 25
totalTime = 0
avgTime = 0
counter = 0
progress_counter = 0

def performPaschTrades(system, pairs):
    global totalTime, avgTime, counter, progress_counter
    maxes = []
    paschCycles = []
    pairsToUpdate = set()

    for pair in pairs:
        a, b = pair
        ret = graph.cycleFromPair(a, b, system)
        maxes.append(ret[0])
        paschCycles.append(ret[1])
        pairsToUpdate.update(set(itertools.chain(*ret[1])))

    maximum = max(maxes)

    for paschCycle in paschCycles:
        combin = list(itertools.combinations(paschCycle, 2))
        for a, b in combin:
            progress_counter += 1
            if progress_counter % 1000 == 0:
                print(f"Working on system: {system}")
                print(f"Progress: {progress_counter} iterations completed")

            newsys = graph.paschtrade(system, a, b)
            if STSGenerator.isSteinerTripleSystem(list(range(1, v + 1)), newsys):
                newMaxes = []
                updatedPairs = set(itertools.chain(*[graph.cycleFromPair(e, f, newsys)[1] for e, f in pairs if (e, f) in pairsToUpdate or (f, e) in pairsToUpdate]))
                if updatedPairs:
                    newMaxes.extend(max(len(cycle) for cycle in updatedPairs))
                if newMaxes and max(newMaxes) < v - 3:
                    with open("finder.txt", 'a') as file:
                        file.write(f"{newsys}\n")

if __name__ == "__main__":
    system = STSGenerator.generateSteinerTripleSystem(v)
    pairs = list(itertools.combinations(range(1, v + 1), 2))
    performPaschTrades(system, pairs)