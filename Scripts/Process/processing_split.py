import sys
import os
import graph
from STSGenerator import isSteinerTripleSystem
from multiprocessing import Pool, Value, Lock, Manager
from functools import partial
from tqdm import tqdm  # Import tqdm for progress bar
import signal  # Import signal for handling interrupts
import logging

def process_chunk(bits):
    """
    Worker function to process a chunk of bitstrings.

    Args:
        bits (list of str): List of bitstrings representing the system.

    Returns:
        tuple: (is_valid (bool), currSystem (list of sets or None))
    """
    try:
        # Convert bitstrings to currSystem
        currSystem = []
        for bitstring in bits:
            currBlock = set()
            for idx, char in enumerate(bitstring):
                if char == "1":
                    currBlock.add(idx + 1)
            currSystem.append(currBlock)

        # Check if it's a Steiner Triple System
        if isSteinerTripleSystem(list(range(1, 22)), currSystem):
            maxCycle = graph.processSystem(currSystem)
            if maxCycle < 18:
                return (True, currSystem)
        return (False, None)
    except Exception as e:
        # Log the exception and return invalid
        logging.error(f"Error processing chunk: {e}")
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
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

    # Initialize counters using Manager
    manager = Manager()
    valid = Value('i', 0)
    invalid = Value('i', 0)
    lock_print = Lock()

    # Directory containing split files
    split_files_dir = "C:/Users/DSU Student/OneDrive/School/Research/Data/Symmetric Order 21/split_files"
    split_files = sorted([
        os.path.join(split_files_dir, f) for f in os.listdir(split_files_dir)
        if f.startswith('decompressed_part') and f.endswith('.txt')
    ])

    if not split_files:
        logging.error(f"No split files found in '{split_files_dir}'. Please ensure the split files are present.")
        sys.exit(1)

    # Initialize multiprocessing Pool with limited processes and initializer to handle signals
    num_workers = min(8, os.cpu_count())  # Adjust based on your system
    pool = Pool(processes=num_workers, initializer=init_worker)

    # Flag to indicate if an interrupt was received
    interrupted = False

    # Define a signal handler for graceful shutdown
    def signal_handler(sig, frame):
        nonlocal interrupted
        interrupted = True
        logging.info("\nInterrupt received! Shutting down gracefully...")
        pool.terminate()  # Terminate worker processes immediately
        pool.join()
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Open the output file once in append mode with buffering
        with open("out.txt", "a", buffering=1) as file_handle:
            # Initialize tqdm progress bar with estimated total systems
            systems_per_split = 1000  # Should match the splitting script
            estimated_total = systems_per_split * len(split_files)
            pbar = tqdm(total=estimated_total, desc="Processing Systems", unit="system")

            for split_file in split_files:
                logging.info(f"Processing {split_file}...")
                current_system_bitstrings = []

                with open(split_file, "r") as infile:
                    for line_num, line in enumerate(infile, 1):
                        line = line.strip()

                        if not line:
                            continue  # Skip empty lines

                        # Each line is a bitstring
                        bitstring = line
                        current_system_bitstrings.append(bitstring)

                        # Check if we've collected enough bitstrings for a system
                        if len(current_system_bitstrings) == 70:
                            # Submit the system to the multiprocessing pool
                            pool.apply_async(
                                process_chunk,
                                args=(current_system_bitstrings.copy(),),
                                callback=partial(handle_result, valid=valid, invalid=invalid, 
                                                file_handle=file_handle, lock_print=lock_print)
                            )

                            # Update progress bar
                            pbar.update(1)

                            # Reset for the next system
                            current_system_bitstrings = []

                # Handle any remaining bitstrings in the split file
                if len(current_system_bitstrings) == 70:
                    pool.apply_async(
                        process_chunk,
                        args=(current_system_bitstrings.copy(),),
                        callback=partial(handle_result, valid=valid, invalid=invalid, 
                                        file_handle=file_handle, lock_print=lock_print)
                    )
                    pbar.update(1)
                elif len(current_system_bitstrings) > 0:
                    logging.warning(f"Incomplete system in {split_file} with {len(current_system_bitstrings)} bitstrings. It will be skipped.")

            # Close the progress bar
            pbar.close()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if not interrupted:
            # Close the pool and wait for all worker processes to finish
            pool.close()
            pool.join()

    # Final output
    logging.info("\nProcessing Complete.")
    logging.info(f"Valid Systems: {valid.value}")
    logging.info(f"Invalid Systems: {invalid.value}")
    total_processed = valid.value + invalid.value
    if total_processed > 0:
        ratio = valid.value / total_processed
        logging.info(f"Validity Ratio: {ratio:.4f}")
    else:
        logging.info("No systems processed.")

if __name__ == "__main__":
    main()
