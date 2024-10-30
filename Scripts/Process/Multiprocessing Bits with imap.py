import sys
import os
import graph
from STSGenerator import isSteinerTripleSystem
from multiprocessing import Pool, Value, Lock, cpu_count
from functools import partial
from tqdm import tqdm
import signal

def process_chunk(bits):
    """
    Worker function to process a chunk of bits.

    Args:
        bits (list of str): List of bit strings representing the system.

    Returns:
        tuple: (is_valid (bool), currSystem (list of sets or None))
    """
    try:
        # Convert bits to workable system
        currSystem = []
        for line in bits:
            currBlock = []
            for char in range(len(line)):
                if line[char] == "1":
                    currBlock.append(char + 1)
            currSystem.append(set(currBlock))

        # Check if it's a valid STS and process the system
        if isSteinerTripleSystem(list(range(1, 22)), currSystem):
            maxCycle = graph.processSystem(currSystem)
            if maxCycle < 18:
                return (True, currSystem)
        return (False, None)
    except Exception as e:
        return (False, None)

def handle_result(result, valid, invalid, file_handle, lock_print):
    """
    Handle the result returned by the worker process.

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

def parse_decompressed_file(input_file_path, total_expected):
    """
    Generator that parses the input file and yields chunks of bits.

    Args:
        input_file_path (str): Path to the input file.
        total_expected (int): Total number of chunks expected.

    Yields:
        list of str: A chunk of 70 bit strings.
    """
    have_prev = False
    soln_size = 0
    orbs = {}
    orblens = {}
    soln = []
    chunk = []

    with open(input_file_path, "r") as input_file:
        for line in input_file:
            line = line.strip()

            if line.startswith("$"):
                # Process orbit definitions
                parts = line.split(maxsplit=1)
                if len(parts) < 2:
                    continue  # Skip malformed lines
                key_str, value = parts
                try:
                    key = int(key_str[1:])  # remove the $ sign and convert to integer
                except ValueError:
                    continue  # Skip lines with invalid keys

                if have_prev:
                    soln_size = 0
                    orbs.clear()
                    orblens.clear()
                    have_prev = False

                orbs[key] = value
                orblens[key] = len(value.split())
            else:
                # Process solution lines
                try:
                    a = list(map(int, line.split()))
                except ValueError:
                    continue  # Skip lines with invalid integers

                total_len = 0
                for x in a:
                    if x not in orbs:
                        # Orbit key not found, skip this solution
                        total_len = 0
                        break
                    total_len += orblens.get(x, 0)

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
                    orbit_key = soln[i]
                    if orbit_key not in orbs:
                        continue  # Skip if orbit key is missing
                    b = orbs[orbit_key].split()
                    for item in b:
                        chunk.append(item)
                        if len(chunk) == 70:
                            yield chunk.copy()
                            chunk.clear()
    
    # After processing all lines, yield any remaining chunk
    if chunk:
        yield chunk.copy()

def main():
    # Initialize shared counters
    valid = Value('i', 0)
    invalid = Value('i', 0)
    lock_print = Lock()

    total_expected = 62336617  # Total number of chunks expected

    # Initialize multiprocessing Pool with limited processes and initializer to handle signals
    num_workers = min(6, cpu_count()) 
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
        # Open the output file once in append mode with line buffering
        with open("out.txt", "a", buffering=1) as file_handle:
            # Define the input file path
            input_file_path = "decompressed.txt"
            if not os.path.exists(input_file_path):
                print(f"Error: '{input_file_path}' not found.")
                pool.close()
                pool.join()
                sys.exit(1)

            # Initialize the parsing generator
            chunk_gen = parse_decompressed_file(input_file_path, total_expected)

            # tdqm progress bar
            pbar = tqdm(total=total_expected, desc="Processing Chunks", unit="chunk",
                        mininterval=0.5, miniters=1000, unit_scale=True)

            # Create a partial function for handling results
            handle_result_partial = partial(
                handle_result,
                valid=valid,
                invalid=invalid,
                file_handle=file_handle,
                lock_print=lock_print
            )

            chunksize = 100

            # Use imap_unordered to process chunks as they are parsed
            for result in pool.imap_unordered(process_chunk, chunk_gen, chunksize=chunksize):
                handle_result_partial(result)
                pbar.update(1)

            pbar.close()

    except KeyboardInterrupt:
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
