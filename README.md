# Steiner Triple System Research Project

Set up for a research project involing Steiner Triple Systems. Research in collaboration with Dr. Schroeder through Dakota State University.

## Description
This project implements algorithms for generating and analyzing Steiner Triple Systems, including the hill-climbing method using Stinson's Algorithm laid out in *Combinatorial Algorithms: Generation, Enumeration, and Design*. 

## Publication
We published a paper! Check it out [here](https://doi.org/10.1016/j.disc.2026.115061)

## Usage
- Using the `main.py` file, you can generate any number of any order of Steiner Triple Systems
- Using the `processSystem` method in the `graph.py` file, you can find the maximum simple cycle length (called the circumference) of a given system
- Using the `externalwriting` method in the `ExternalWriting` module, you can continuously generate systems and record information about the current system in output files

## Project Structure
- Contains a `Scripts` folder which houses all the code
    - `Process` folder contains all scripts that were helpful in the process of creating the current systems, but are currently unused
    - `main.py` handles simple generation of a given number of a given order of Steiner Triple Systems
    - `STSGenerator.py` handles the actual generation of the systems
    - `graph.py` is the graph module (using networkx) that handles the analysis of a given system (finding circumference of system)
    - `Multiprocessing_bits.py` was designed to analyze the $6233617$ systems with perscribed groups of automorphisms from [this paper](https://doi.org/10.1137/S0895480104444788) by Petteri Kaski
    - `STS21_vectorization.py` is a script that takes in a text file containing STS21s and analyzes their cycles and outputs their "cycle vectors" (defined more clearly in the script's documentation)
    - `ExternalWriting.py` contains all the methods used for writing mass numbers of generated STS of a given order to a CSV format.
    - `PaschChecker.py` is a script designed to analyze a file full of STS and tally up which systems are Anti-Pasch and vice-versa
- Contains a `Results` folder which houses an example output file that the `ExternalWriting.py` script would generate and a folder called `Presentation` containing all pertinent materials to a presentation I gave about Steiner Triple Systems and my work on this project.
- Contains a `Documentation` folder which houses all documentation (information about methodologies and algorithms used in this project)

## Acknowledgments
- Dr. Justin Schroeder at Dakota State University as my mentor for this project
- Petteri Kaski from Aalto University for generous sharing of information from his publications
