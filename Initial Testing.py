# Define a function to check if a set of points and triples is a Steiner triple system
def is_steiner_triple_system(points, triples):
    # Check if every pair of points appears in exactly one triple
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pair = {points[i], points[j]}
            count = 0
            for triple in triples:
                if pair.issubset(triple):
                    count += 1
            if count != 1:
                return False
    # Check if the order of the system is congruent to 1 or 3 modulo 6
    order = len(points)
    if order % 6 not in [1, 3]:
        return False
    # Return True if all checks passed
    return True

# Example of a valid Steiner triple system of order 7
points = [1, 2, 3, 4, 5, 6, 7]
triples = [{1, 2, 3}, {1, 4, 5}, {1, 6, 7}, {2, 4, 6}, {2, 5, 7}, {3, 4, 7}, {3, 5, 6}]
print(is_steiner_triple_system(points, triples)) # True

# Example of an invalid Steiner triple system of order 8
points = [1, 2, 3, 4, 5, 6, 7, 8]
triples = [{1, 2, 3}, {1, 4, 5}, {1, 6, 7}, {2, 4, 6}, {2, 5, 7}, {3, 4, 7}, {3, 5, 6}, {1, 8, 9}]
print(is_steiner_triple_system(points, triples)) # False
