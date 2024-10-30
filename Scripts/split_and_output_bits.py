import os
import time

def printProgressBar(iteration, total, start_time, length=50):
    """
    Displays a progress bar in the terminal.
    
    Args:
        iteration (int): Current iteration.
        total (int): Total iterations.
        start_time (float): Start time of the process.
        length (int): Length of the progress bar.
    """
    progress = int(length * iteration // total)
    bar = '█' * progress + '-' * (length - progress)
    percent = (iteration / total) * 100 if total > 0 else 0

    elapsed_time = time.time() - start_time
    estimated_total_time = (elapsed_time * total / iteration) if iteration > 0 else 0
    remaining_time = estimated_total_time - elapsed_time

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\r|{bar}| {percent:.2f}% complete, ETA: {remaining_time:.2f} seconds", end='\r')
    if iteration >= total:
        print()  # Move to the next line

def systemFromBits(bits, start_time, output_file_handle):
    """
    Writes a system's bitstrings to the output file.
    
    Args:
        bits (list of str): List of 70 bitstrings representing the system.
        start_time (float): Start time of the process.
        output_file_handle (file object): File handle to write the bitstrings.
    """
    # Write each bitstring to the output file
    for bitstring in bits:
        output_file_handle.write(f"{bitstring}\n")
    
    #blank line to separate systems
    output_file_handle.write("\n")

    # Update progress every 100 systems
    global systems_processed
    systems_processed += 1
    if systems_processed % 10000 == 0:
        printProgressBar(systems_processed, total_systems, start_time)

if __name__ == "__main__":
    have_prev = False
    soln_size = 0
    orbs = {}
    orblens = {}
    soln = []
    chunk = []
    start_time = time.time()

    # Split parameters
    SYSTEMS_PER_SPLIT = 100000  # Number of systems per split file
    split_file_count = 1
    systems_in_current_file = 0
    output_directory = "split_files"

    # counter for progress tracking
    systems_processed = 0

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")

    # Initialize the first output file
    output_filename = os.path.join(output_directory, f"out_part{split_file_count}.txt")
    output_file = open(output_filename, "w")
    print(f"Created {output_filename}")

    
    total_systems = 62336617

    # Reset the orbs dictionaries for actual processing
    orbs.clear()
    orblens.clear()

    # Start processing the file
    with open("decompressed.txt", "r") as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if line.startswith("$"):
                parts = line.split(maxsplit=1)
                if len(parts) < 2:
                    print(f"Line {line_num} is malformed: '{line}'")
                    continue  # Skip malformed lines
                key = int(parts[0][1:])  # Remove the $ sign and convert to integer
                value = parts[1]

                if have_prev:
                    soln_size = 0
                    orbs.clear()
                    orblens.clear()
                    have_prev = False

                orbs[key] = value
                orblens[key] = len(value.split())

            else:
                try:
                    a = list(map(int, line.split()))
                except ValueError:
                    print(f"Line {line_num} contains non-integer values: '{line}'")
                    continue  # Skip lines with invalid integers

                total_len = 0

                # Calculate total length of orbits
                try:
                    for x in a:
                        if x not in orbs:
                            raise ValueError(f"Orbit {x} not known at line {line_num}")
                        total_len += orblens[x]
                except ValueError as e:
                    print(e)
                    continue  # Skip lines with unknown orbits

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

                # Output matrix in usable form
                for i in range(soln_size):
                    b = orbs[soln[i]].split()
                    for item in b:
                        chunk.append(item)
                        if len(chunk) == 70:
                            systemFromBits(chunk, start_time, output_file)
                            chunk.clear()  # Resetting chunk for next group
                            systems_in_current_file += 1

                            # Check if we need to create a new split file
                            if systems_in_current_file >= SYSTEMS_PER_SPLIT:
                                output_file.close()
                                split_file_count += 1
                                systems_in_current_file = 0
                                output_filename = os.path.join(output_directory, f"out_part{split_file_count}.txt")
                                output_file = open(output_filename, "w")
                                print(f"Created {output_filename}")

    # After processing all lines, handle any remaining chunk
    if chunk:
        if len(chunk) == 70:
            systemFromBits(chunk, start_time, output_file)
            systems_in_current_file += 1
            # Check if a new split file needs to be created
            if systems_in_current_file >= SYSTEMS_PER_SPLIT:
                output_file.close()
                split_file_count += 1
                systems_in_current_file = 0
                output_filename = os.path.join(output_directory, f"out_part{split_file_count}.txt")
                output_file = open(output_filename, "w")
                print(f"Created {output_filename}")
        else:
            print(f"Incomplete system with {len(chunk)} bitstrings found at the end of the file. It will be skipped.")

    # Close the last output file
    output_file.close()
    print("Bitstrings have been successfully split into multiple files.")
    print(f"Total systems processed: {systems_processed}")
    print(f"Processing completed in {time.time() - start_time:.2f} seconds.")
