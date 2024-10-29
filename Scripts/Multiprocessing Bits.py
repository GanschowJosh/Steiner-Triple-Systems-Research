import sys
import os
import graph
from STSGenerator import isSteinerTripleSystem
from multiprocessing import Pool, Manager, Value, Lock
from functools import partial
from tqdm import tqdm  # Import tqdm for progress bar
import signal  # Import signal for handling interrupts

def process_chunk(bits):
    """
    Worker function to process a chunk of bits.

    Args:
        bits (list of str): List of bit strings representing the system.

    Returns:
        tuple: (is_valid (bool), currSystem (list of sets or None))
    """
    try:
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
    except Exception as e:
        # Log the exception and return invalid
        return (False, None)

def handle_result(result, valid, invalid, file_handle, lock_print):
    """
    Callback function to handle results from worker processes.

    Args:
        result (tuple): (is_valid (bool), currSystem (list of sets or None))
        valid (Value): Shared value for counting valid systems.
        invalid (Value): Shared value for counting invalid systems.
        file_handle (file object): File handle to write valid systems.
        lock_print (Lock): Lock to synchronize console output.
    """
    is_valid, currSystem = result
    if is_valid:
        with valid.get_lock():
            valid.value += 1
        # Write to file without storing in memory
        with lock_print:
            file_handle.write(f"{currSystem}\n")
    else:
        with invalid.get_lock():
            invalid.value += 1

def init_worker():
    """
    Ignore SIGINT in worker processes to allow graceful shutdown from the main process.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def main():
    # Initialize counters using Manager
    manager = Manager()
    valid = Value('i', 0)
    invalid = Value('i', 0)
    lock_print = Lock()

    # Define total expected for progress bar (adjust as needed)
    total_expected = 62336617  # Total number of chunks expected
    processed = 0

    # Variables for parsing input
    have_prev = False
    soln_size = 0
    orbs = {}
    orblens = {}
    soln = []
    counter = 0
    chunk = []

    # Initialize multiprocessing Pool with limited processes and initializer to handle signals
    num_workers = min(8, os.cpu_count())  # Adjust based on your system
    pool = Pool(processes=num_workers, initializer=init_worker)

    # Flag to indicate if an interrupt was received
    interrupted = False

    # Define a signal handler for graceful shutdown
    def signal_handler(sig, frame):
        nonlocal interrupted
        interrupted = True
        print("\nInterrupt received! Shutting down gracefully...")
        pool.terminate()  # Terminate worker processes immediately
        pool.join()
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Open the output file once in append mode with buffering
        with open("out.txt", "a", buffering=1) as file_handle:
            # Open and read from 'decompressed.txt'
            input_file_path = "decompressed.txt"
            if not os.path.exists(input_file_path):
                print(f"Error: '{input_file_path}' not found.")
                pool.close()
                pool.join()
                sys.exit(1)

            with open(input_file_path, "r") as input_file:
                # Initialize tqdm progress bar
                pbar = tqdm(total=total_expected, desc="Processing Chunks", unit="chunk")

                for line in input_file:
                    line = line.strip()

                    # Print the first 100 lines for debugging
                    """if counter < 100:
                        print(line)
                        counter += 1"""

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
                                raise ValueError(f"Orbit {x} not known")
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
                                        callback=partial(handle_result, valid=valid, invalid=invalid, file_handle=file_handle, lock_print=lock_print)
                                    )
                                    chunk.clear()
                                    processed += 1
                                    pbar.update(1)

                # After processing all lines, handle any remaining chunk
                if chunk:
                    pool.apply_async(
                        process_chunk,
                        args=(chunk.copy(),),
                        callback=partial(handle_result, valid=valid, invalid=invalid, file_handle=file_handle, lock_print=lock_print)
                    )
                    processed += 1
                    pbar.update(1)

                # Close the progress bar
                pbar.close()

    except KeyboardInterrupt:
        # This block will not be reached because the signal handler exits the program
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if not interrupted:
            # Close the pool and wait for all worker processes to finish
            pool.close()
            pool.join()

    # Final output
    print("\nProcessing Complete.")
    print(f"Valid Systems: {valid.value}")
    print(f"Invalid Systems: {invalid.value}")
    if (valid.value + invalid.value) > 0:
        ratio = valid.value / (valid.value + invalid.value)
        print(f"Validity Ratio: {ratio:.4f}")
    else:
        print("No systems processed.")

if __name__ == "__main__":
    main()
