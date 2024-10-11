li = []
for i in range(70):
    li.append(input())

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
                print(f"Pair {pair} appears in {count} triples, which is incorrect.")
                for triple in triples_set:
                    if pair.issubset(triple):
                        print(f"Found in triple: {triple}")
                return False

    # Check that each triple has exactly 3 points
    for triple in triples_set:
        if len(triple) != 3:
            print(f"Triple {triple} does not have exactly 3 points.")
            return False

    # Check if the order of the system is congruent to 1 or 3 modulo 6
    order = len(points)
    if order % 6 not in [1, 3]:
        print(f"Order of the system is {order}, which is not congruent to 1 or 3 modulo 6.")
        return False

    # Return True if all checks passed
    print("The system is a valid Steiner Triple System.")
    return True

while True:
    system = []
    for item in li:
        currBlock = []
        for i in range(len(item)):
            if item[i] == "1":
                currBlock.append(i+1)
        system.append(set(currBlock))
    print(isSteinerTripleSystem(list(i+1 for i in range(21)), system))