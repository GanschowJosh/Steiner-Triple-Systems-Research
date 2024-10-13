"""
Main file for simple generation of a given number 
of Steiner Triple Systems of a given order
"""
from STSGenerator import generateSteinerTripleSystem, isSteinerTripleSystem

order = int(input("What order of STS would you like to generate? "))
numSystems = int(input("How many systems would you like to generate? "))

if numSystems > 0:
    for i in range(numSystems):
        STS = generateSteinerTripleSystem(order)
        print(STS, end=f"\n{"="*20}\n")
