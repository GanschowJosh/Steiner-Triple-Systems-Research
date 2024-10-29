import sys
import os
import graph
from STSGenerator import isSteinerTripleSystem
from multiprocessing import Pool, Manager, Value
import time  # Import time module for tracking elapsed time

def printProgressBar(iteration, total, start_time, length=50):
    """
    Displays or updates a console progress bar with estimated time remaining.

    Args:
        iteration (int): Current iteration count.
        total (int): Total number of iterations.
        start_time (float): Timestamp when processing started.
        length (int, optional): Length of the progress bar. Defaults to 50.
    """
    progress = int(length * iteration // total)
    bar = '█' * progress + '-' * (length - progress)
    percent = (iteration / total) * 100

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Calculate estimated total time
    if iteration > 0:
        time_per_chunk = elapsed_time / iteration
        estimated_total_time = time_per_chunk * total
        remaining_time = estimated_total_time - elapsed_time
    else:
        remaining_time = 0

    # Format remaining time into H:M:S
    hrs, rem = divmod(int(remaining_time), 3600)
    mins, secs = divmod(rem, 60)
    time_format = f"{hrs}h {mins}m {secs}s"

    # Clear the console and print the progress bar with time estimation
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\r|{bar}| {percent:.2f}% complete | Time Left: {time_format}", end='')

def process_chunk(bits):
    """
    Worker function to process a chunk of bits.

    Args:
        bits (list of str): List of bit strings representing the system.

    Returns:
        tuple: (is_valid (bool), currSystem (list of sets or None))
    """
    # Convert bits to currSystem
    currSystem = []
    for line in bits:
        currBlock = []
        for char in range(len(line)):
            if line[char] == "1":
                currBlock.append(char + 1)
        currSystem.append(set(currBlock))

    # Check if it's a Steiner Triple System
    if isSteinerTripleSystem(list(range(1, 22)), currSystem):
        maxCycle = graph.processSystem(currSystem)
        if maxCycle < 18:
            return (True, currSystem)
    return (False, None)

def handle_result(result, valid, invalid, best, file_handle):
    """
    Callback function to handle results from worker processes.

    Args:
        result (tuple): (is_valid (bool), currSystem (list of sets or None))
        valid (Value): Shared value for counting valid systems.
        invalid (Value): Shared value for counting invalid systems.
        best (list): Shared list to store best systems.
        file_handle (file object): File handle to write valid systems.
    """
    is_valid, currSystem = result
    if is_valid:
        with valid.get_lock():
            valid.value += 1
        best.append(currSystem)
        file_handle.write(f"{currSystem}\n")
        print(currSystem)
    else:
        with invalid.get_lock():
            invalid.value += 1

def main():
    # Initialize counters and storage using Manager
    manager = Manager()
    best = manager.list()
    valid = Value('i', 0)
    invalid = Value('i', 0)
    
    # Define total expected for progress bar (adjust as needed)
    total_expected = 62336617  # Total number of chunks expected
    processed = Value('i', 0)

    # Record the start time
    start_time = time.time()

    # Variables for parsing input
    have_prev = False
    soln_size = 0
    orbs = {}
    orblens = {}
    soln = []
    counter = 0
    chunk = []

    # Initialize multiprocessing Pool
    pool = Pool()

    # Open the output file once in append mode
    with open("out.txt", "a") as file_handle:
        # Open and read from 'decompressed.txt'
        try:
            with open("decompressed.txt", "r") as input_file:
                for line in input_file:
                    line = line.strip()

                    # Print the first 100 lines for debugging
                    if counter < 100:
                        print(line)
                        counter += 1

                    if line.startswith("$"):
                        # Process orbit definitions
                        parts = line.split(maxsplit=1)
                        key = int(parts[0][1:])  # remove the $ sign and convert to integer
                        value = parts[1]

                        if have_prev:
                            soln_size = 0
                            orbs.clear()
                            orblens.clear()
                            have_prev = False

                        orbs[key] = value
                        orblens[key] = len(value.split())

                    else:
                        # Process solution lines
                        a = list(map(int, line.split()))
                        total_len = 0

                        # Calculate total length of orbits
                        for x in a:
                            if x not in orbs:
                                raise ValueError("Orbit not known")
                            total_len += orblens[x]

                        if have_prev:
                            j = soln_size - 1
                            while total_len > 0 and j >= 0:
                                total_len -= orblens.get(soln[j], 0)
                                j -= 1
                            j += 1
                        else:
                            j = 0

                        soln_size = j + len(a)

                        # Update solution array
                        for i in range(len(a)):
                            if len(soln) > j:
                                soln[j] = a[i]
                            else:
                                soln.append(a[i])
                            j += 1

                        have_prev = True

                        # Convert solution to usable form and build chunks
                        for i in range(soln_size):
                            b = orbs[soln[i]].split()
                            for item in b:
                                chunk.append(item)
                                if len(chunk) == 70:
                                    # Submit the chunk to the multiprocessing pool
                                    pool.apply_async(
                                        process_chunk,
                                        args=(chunk.copy(),),
                                        callback=lambda res: handle_result(res, valid, invalid, best, file_handle)
                                    )
                                    chunk.clear()
                                    with processed.get_lock():
                                        processed.value += 1

                                    # Update progress bar every 250 processed chunks
                                    if processed.value % 250 == 0:
                                        printProgressBar(processed.value, total_expected, start_time)
                                        print(f"\nProcessed Chunks: {processed.value}")
        except FileNotFoundError as e:
            print(e)
            pool.close()
            pool.join()
            sys.exit(1)

        # After processing all lines, handle any remaining chunk
        if chunk:
            pool.apply_async(
                process_chunk,
                args=(chunk.copy(),),
                callback=lambda res: handle_result(res, valid, invalid, best, file_handle)
            )
            with processed.get_lock():
                processed.value += 1

        # Final progress bar update after all chunks are submitted
        printProgressBar(processed.value, total_expected, start_time)
        print(f"\nProcessed Chunks: {processed.value}")

        # Close the pool and wait for all worker processes to finish
        pool.close()
        pool.join()

    # Final output
    print("\nProcessing Complete.")
    print(f"Best Systems Found: {len(best)}")
    print(f"Valid Systems: {valid.value}")
    print(f"Invalid Systems: {invalid.value}")
    if (valid.value + invalid.value) > 0:
        print(f"Validity Ratio: {valid.value / (valid.value + invalid.value):.4f}")
    else:
        print("No systems processed.")

if __name__ == "__main__":
    main()
