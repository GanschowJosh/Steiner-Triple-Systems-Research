# Define a function to check if a set of points and triples is a Steiner triple system
def isSteinerTripleSystem(points, triples):
    # Create a set of all triples
    triples_set = set(map(frozenset, triples))

    # Check if every pair of points appears in exactly one triple
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pair = frozenset([points[i], points[j]])
            count = sum(1 for triple in triples_set if pair <= triple)
            if count != 1:
                return False

    # Check if the order of the system is congruent to 1 or 3 modulo 6
    order = len(points)
    if order % 6 not in [1, 3]:
        return False

    # Return True if all checks passed
    return True


# Example of a valid Steiner triple system of order 9
points = [1, 2, 3, 4, 5, 6, 7, 8, 9]
triples = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{2,6,7},{3,4,8},{1,6,8},{2,4,9},{3,5,7}]	

print(isSteinerTripleSystem(points, triples)) # True

# Example of an invalid Steiner triple system of order 8
points = [1, 2, 3, 4, 5, 6, 7, 8]
triples = [{1, 2, 3}, {1, 4, 5}, {1, 6, 7}, {2, 4, 6}, {2, 5, 7}, {3, 4, 7}, {3, 5, 6}, {1, 8, 9}]
print(isSteinerTripleSystem(points, triples)) # False
