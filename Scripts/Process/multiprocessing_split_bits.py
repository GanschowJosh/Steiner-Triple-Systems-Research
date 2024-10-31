import sys
import os
import glob
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
        currSystem = [
            {char + 1 for char, bit in enumerate(line) if bit == "1"}
            for line in bits
        ]

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
            # Format the system for readability, e.g., one set per line
            system_str = '\n'.join(['{' + ', '.join(map(str, sorted(s))) + '}' for s in currSystem])
            file_handle.write(f"{system_str}\n\n")  # Separate systems by a blank line
    else:
        with invalid.get_lock():
            invalid.value += 1

def init_worker():
    """
    Ignore SIGINT in worker processes to allow graceful shutdown from the main process.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def main():
    # Directory containing the split text files
    input_dir = "C:/Users/DSU Student/OneDrive/School/Research/Data/Symmetric Order 21/split_files"  
    output_file = "out2.txt"  # Output file to store valid systems
    total_expected = 62336617  # Total number of systems expected

    # Find all .txt files in the input directory
    input_files = glob.glob(os.path.join(input_dir, "*.txt"))
    if not input_files:
        print(f"No .txt files found in directory '{input_dir}'. Exiting.")
        sys.exit(1)

    # Initialize counters using Manager
    manager = Manager()
    valid = Value('i', 0)
    invalid = Value('i', 0)
    lock_print = Lock()

    # Initialize multiprocessing Pool with limited processes and initializer to handle signals
    num_workers = min(6, os.cpu_count())  # Adjust based on your system
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
        with open(output_file, "a", buffering=1) as file_handle:
            # Initialize tqdm progress bar without a predefined total
            pbar = tqdm(total=total_expected, desc="Processing Systems", unit="system")

            for input_file_path in input_files:
                if not os.path.exists(input_file_path):
                    print(f"Warning: '{input_file_path}' does not exist. Skipping.")
                    continue

                with open(input_file_path, "r") as input_file:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"Processing '{input_file_path}'...")
                    system = []
                    for line in input_file:
                        stripped_line = line.strip()

                        if stripped_line == "":
                            # Blank line indicates the end of a system
                            if len(system) == 70:
                                # Submit the system to the multiprocessing pool
                                pool.apply_async(
                                    process_chunk,
                                    args=(system.copy(),),
                                    callback=partial(
                                        handle_result,
                                        valid=valid,
                                        invalid=invalid,
                                        file_handle=file_handle,
                                        lock_print=lock_print
                                    )
                                )
                                pbar.update(1)
                            elif len(system) > 0:
                                print(f"Warning: Incomplete system with {len(system)} bitstrings in '{input_file_path}'. Skipping.")
                            system.clear()
                        else:
                            system.append(stripped_line)

                    # After reading all lines, check if there's a remaining system
                    if len(system) == 70:
                        pool.apply_async(
                            process_chunk,
                            args=(system.copy(),),
                            callback=partial(
                                handle_result,
                                valid=valid,
                                invalid=invalid,
                                file_handle=file_handle,
                                lock_print=lock_print
                            )
                        )
                        pbar.update(1)
                    elif len(system) > 0:
                        print(f"Warning: Incomplete system with {len(system)} bitstrings in '{input_file_path}'. Skipping.")

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
