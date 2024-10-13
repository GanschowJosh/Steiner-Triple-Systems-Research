import random
import hashlib
import json
from itertools import permutations
import time
import Scripts.graph as graph 

def canonicalForm(S, T):
    startTime = time.time()
    # Generate all permutations of S
    perms = permutations(S)
    
    # Initialize the canonical form to be the lexicographically first triple system
    canonicalT = sorted(sorted(triple) for triple in T)
    
    for perm in perms:
        # Create a mapping from the original points to the permuted points
        alpha = {S[i]: perm[i] for i in range(len(S))}
        
        # Apply the permutation to T
        tPerm = [{alpha[point] for point in triple} for triple in T]
        tPerm = sorted(sorted(triple) for triple in tPerm)

        
        # Update the canonical form if necessary
        if tPerm < canonicalT:
            canonicalT = tPerm
    
    print(f"Time taken to find canonical form: {time.time() - startTime:.5f} seconds")

    return canonicalT

def generateKey(S, T):
    # Generate the canonical form of the STS
    canonicalT = canonicalForm(S, T)
    
    # Serialize the canonical form
    serializedT = json.dumps(canonicalT).encode('utf-8')
    
    # Generate a SHA-256 hash of the serialized canonical form
    hashObject = hashlib.sha256(serializedT)
    return hashObject.hexdigest()