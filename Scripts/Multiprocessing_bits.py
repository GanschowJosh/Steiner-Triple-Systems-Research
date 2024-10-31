import sys
import os
import graph
from STSGenerator import isSteinerTripleSystem
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Value, Lock
from functools import partial
from tqdm import tqdm
import signal

def process_chunk(bits):
    """
    Optimized worker function to process a chunk of bits.

    Args:
        bits (list of str): List of bit strings representing the system.

    Returns:
        tuple: (is_valid (bool), currSystem (list of sets or None))
    """
    try:
        # Convert bits to currSystem using list comprehensions for speed
        currSystem = [
            {char + 1 for char, bit in enumerate(line) if bit == "1"}
            for line in bits
        ]

        # Check if it's an STS and process the system
        if isSteinerTripleSystem(list(range(1, 22)), currSystem):
            maxCycle = graph.processSystem(currSystem)
            if maxCycle < 18:
                return (True, currSystem)
        return (False, None)
    except Exception as e:
        return (False, None)

def result_handler(future, valid, invalid, file_handle, lock_print):
    """
    Handles the result of a processed chunk.

    Args:
        future (Future): Future object containing the result.
        valid (Value): Shared value for counting valid systems.
        invalid (Value): Shared value for counting invalid systems.
        file_handle (file object): File handle to write valid systems.
        lock_print (Lock): Lock to synchronize file writes.
    """
    try:
        is_valid, currSystem = future.result()
        if is_valid:
            with valid.get_lock():
                valid.value += 1
            # Write to file without storing in memory
            with lock_print:
                file_handle.write(f"{currSystem}\n")
        else:
            with invalid.get_lock():
                invalid.value += 1
    except Exception as e:
        pass

def init_worker():
    """
    Ignore SIGINT in worker processes to allow graceful shutdown from the main process.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def main():
    # Initialize shared counters
    valid = Value('i', 0)
    invalid = Value('i', 0)
    lock_print = Lock()

    total_expected = 62336617  # Total number of chunks expected

    # Variables for parsing input
    have_prev = False
    soln_size = 0
    orbs = {}
    orblens = {}
    soln = []
    chunk = []
    processed = 0

    num_workers = max(1, min(os.cpu_count() - 1, 12))

    max_concurrent_futures = 10000

    active_futures = set()

    # Flag to indicate if an interrupt was received
    interrupted = False

    # Define a signal handler for graceful shutdown (still doesn't work lol)
    def signal_handler(sig, frame):
        nonlocal interrupted
        interrupted = True
        print("\nInterrupt received! Shutting down gracefully...")
        executor.shutdown(wait=False, cancel_futures=True)
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    try:
        with open("out.txt", "a", buffering=1) as file_handle:
            input_file_path = "../Data/Symmetric Order 21/decompressed.txt"
            if not os.path.exists(input_file_path):
                print(f"Error: '{input_file_path}' not found.")
                sys.exit(1)

            with open(input_file_path, "r") as input_file:
                pbar = tqdm(total=total_expected, desc="Processing Chunks", unit="systems", miniters=1000, unit_scale=True)

                with ProcessPoolExecutor(max_workers=num_workers, initializer=init_worker) as executor:
                    # Keep track of active futures
                    for line in input_file:
                        line = line.strip()

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
                                        # Prepare the batch
                                        batch = chunk.copy()
                                        chunk.clear()

                                        # Submit the batch to the process pool
                                        future = executor.submit(process_chunk, batch)
                                        active_futures.add(future)

                                        # Attach a callback to handle the result
                                        future.add_done_callback(
                                            partial(result_handler, valid=valid, invalid=invalid, file_handle=file_handle, lock_print=lock_print)
                                        )

                                        processed += 1
                                        pbar.update(1)

                                        # If maximum concurrent futures reached, wait for some to complete
                                        if len(active_futures) >= max_concurrent_futures:
                                            done, active_futures = wait(active_futures, return_when='FIRST_COMPLETED')
                    
                    # After processing all lines, handle any remaining chunk
                    if chunk:
                        batch = chunk.copy()
                        chunk.clear()
                        future = executor.submit(process_chunk, batch)
                        active_futures.add(future)
                        future.add_done_callback(
                            partial(result_handler, valid=valid, invalid=invalid, file_handle=file_handle, lock_print=lock_print)
                        )
                        processed += 1
                        pbar.update(1)

                    # Wait for all remaining futures to complete
                    while active_futures:
                        done, active_futures = wait(active_futures, return_when='FIRST_COMPLETED')

                    # Close the progress bar
                    pbar.close()

    except KeyboardInterrupt:
        # Handled by the signal handler
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if not interrupted:
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
    from concurrent.futures import wait  # Import here to avoid issues with multiprocessing
    main()
