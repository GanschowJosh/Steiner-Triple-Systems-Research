import sys
from itertools import combinations
from collections import defaultdict

def read_sts_file(filename):
    """
    Function to read in the STS21 systems from a file and return a list of systems.
    """
    with open(filename, 'r') as file:
        sts21_list = []
        for line in file:
            sts21_list.append(eval(line))
    return sts21_list

def determine_order(triples):
    """
    Determines the order (number of points) of an STS by finding the maximum point number.

    Args:
        triples (list of tuples): List of triples in the STS.

    Returns:
        int: The order of the STS.
    """
    max_point = max(max(triple) for triple in triples)
    return max_point

def validate_sts(triples):
    """
    Validates whether the given triples form a valid Steiner Triple System.

    Args:
        triples (list of tuples): List of triples in the STS.

    Returns:
        tuple: (is_valid (bool), order (int), expected_num_triples (int))
    """
    order = determine_order(triples)
    if order % 6 not in [1, 3]:
        print(f"Warning: Order {order} is not congruent to 1 or 3 mod 6.")
        # Still proceed, as user might have specific reasons.
    expected_num_triples = (order * (order - 1)) // 6
    actual_num_triples = len(triples)
    is_valid = (actual_num_triples == expected_num_triples)
    if not is_valid:
        print(f"Warning: STS of order {order} has {actual_num_triples} triples (expected {expected_num_triples}).")
    return is_valid, order, expected_num_triples

def build_point_to_triples(triples):
    """
    Builds a mapping from each point to the set of triples that include it.

    Args:
        triples (list of tuples): List of triples in the STS.

    Returns:
        dict: A dictionary mapping each point to a set of triples containing it.
    """
    point_to_triples = defaultdict(set)
    for triple in triples:
        triple_fset = frozenset(triple)
        for point in triple:
            point_to_triples[point].add(triple_fset)
    return point_to_triples

def contains_pasch(triples, point_to_triples):
    """
    Determines whether the given STS contains any Pasch configurations.

    Args:
        triples (list of tuples): List of triples in the STS.
        point_to_triples (dict): Mapping from points to triples containing them.

    Returns:
        bool: True if the STS contains at least one Pasch configuration, False otherwise.
    """
    triple_set = set(frozenset(triple) for triple in triples)
    
    # Iterate over all combinations of four triples
    # Optimizing by checking Pasch configurations as defined
    # For each t1, find t2 sharing one point with t1, t3 and t4 accordingly

    for t1 in triple_set:
        a, b, c = sorted(t1)
        # Find triples that share 'a' with t1, excluding t1 itself
        for t2 in point_to_triples[a]:
            if t2 == t1:
                continue
            t2_sorted = sorted(t2)
            # Extract d and e from t2, which must not be in t1
            d, e = [x for x in t2_sorted if x != a]
            if d in t1 or e in t1:
                continue
            # Now, find triples containing both 'b' and 'd', excluding t1 and t2
            possible_t3 = point_to_triples[b].intersection(point_to_triples[d])
            for t3 in possible_t3:
                if t3 == t1 or t3 == t2:
                    continue
                # t3 should be {b, d, f}
                f_candidates = [x for x in t3 if x != b and x != d]
                if not f_candidates:
                    continue
                f = f_candidates[0]
                if f in t1 or f in t2:
                    continue
                # Now, check if {c, e, f} exists in the triple_set
                pasch_triple = frozenset([c, e, f])
                if pasch_triple in triple_set:
                    # Found a Pasch configuration
                    return True
    # No Pasch configuration found
    return False

def check_anti_pasch_systems(sts_list):
    """
    Checks each STS in the list for being anti-Pasch.

    Args:
        sts_list (list of list of tuples): List of STS systems.

    Returns:
        list of dict: Each dictionary contains information about the STS and its anti-Pasch status.
    """
    results = []
    for idx, sts in enumerate(sts_list, 1):
        is_valid, order, expected_triples = validate_sts(sts)
        if not is_valid:
            print(f"STS #{idx}: Invalid STS structure. Skipping Pasch check.")
            results.append({
                'index': idx,
                'is_valid': False,
                'order': order,
                'is_anti_pasch': None,
                'reason': 'Invalid STS structure'
            })
            continue
        point_to_triples = build_point_to_triples(sts)
        has_pasch = contains_pasch(sts, point_to_triples)
        is_anti_pasch = not has_pasch
        results.append({
            'index': idx,
            'is_valid': True,
            'order': order,
            'is_anti_pasch': is_anti_pasch
        })
        status = "Anti-Pasch" if is_anti_pasch else "Contains Pasch"
        print(f"STS #{idx} (Order {order}): {status}")
    return results

def main(input_file, output_file=None):
    """
    Main function to read STS systems from a file and check for anti-Pasch property.

    Args:
        input_file (str): Path to the input file containing STS systems.
        output_file (str, optional): Path to the output file to save results. Defaults to None.
    """
    print(f"Reading STS systems from '{input_file}'...")
    sts_list = read_sts_file(input_file)
    print(f"Total STS systems read: {len(sts_list)}\n")

    print("Validating and checking for anti-Pasch property...\n")
    results = check_anti_pasch_systems(sts_list)

    # Prepare summary
    total_valid = sum(1 for res in results if res['is_valid'])
    total_invalid = len(results) - total_valid
    total_anti_pasch = sum(1 for res in results if res['is_valid'] and res['is_anti_pasch'])
    total_contains_pasch = sum(1 for res in results if res['is_valid'] and not res['is_anti_pasch'])

    summary = f"""
Summary:
--------
Total STS systems processed: {len(sts_list)}
Valid STS systems: {total_valid}
Invalid STS systems: {total_invalid}
Anti-Pasch STS systems: {total_anti_pasch}
STS systems containing Pasch configurations: {total_contains_pasch}
"""

    print(summary)

    if output_file:
        with open(output_file, 'w') as out_file:
            out_file.write("Index,Order,Is_Valid,Is_Anti_Pasch,Reason\n")
            for res in results:
                index = res['index']
                order = res['order']
                is_valid = res['is_valid']
                is_anti_pasch = res['is_anti_pasch']
                reason = res.get('reason', '')
                out_file.write(f"{index},{order},{is_valid},{is_anti_pasch},{reason}\n")
            out_file.write("\n")
            out_file.write(summary)
        print(f"Results have been written to '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python check_anti_pasch_general.py <input_file> [<output_file>]")
        print(" - <input_file>: Path to the input file containing STS systems.")
        print(" - <output_file>: (Optional) Path to the output file to save results.")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else None
    
    main(input_filename, output_filename)
