import os
import Scripts.graph as graph
import Scripts.STSGenerator as STSGenerator
import ast
from multiprocessing import Pool
from Scripts.paschTrades import performPaschTrades

pairs = []
v = 25
for a in range(v, 0, -1):
    for b in range(1, v+1):
        if a!=b:
            pairs.append((a, b))

def worker(line):
    steinerSystem = line.split('}]",')[0][1:] + '}]'
    steinerSystem = ast.literal_eval(steinerSystem)
    performPaschTrades(steinerSystem, pairs)

if __name__ == '__main__':
    '''
    directory = './CycleGeneration'
    i = 0
    j = 0
    for filename in os.listdir(directory):
        i+=1
        with open(os.path.join(directory, filename)) as f:
            j += 1
            lines = f.read().split("\n")[1:]
            with Pool() as p:
                p.map(worker, lines)
            print(f"Working on line #{j}")
        print(f"Done with file #{i}")
    '''
    
    sys = STSGenerator.mainFunc()
    print(sys)
    performPaschTrades(sys, pairs)

