"""Interactively generate one or more Steiner triple systems."""

from STSGenerator import generateSteinerTripleSystem


def main():
    try:
        order = int(input("What order of STS would you like to generate? "))
        num_systems = int(input("How many systems would you like to generate? "))
    except ValueError:
        print("Order and number of systems must be integers.")
        return

    if num_systems < 1:
        print("Number of systems must be positive.")
        return

    try:
        for _ in range(num_systems):
            system = generateSteinerTripleSystem(order)
            print(system)
            print("=" * 20)
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()
