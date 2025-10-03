import sys
import os
from comparer import comparer


def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <file1> <file2>")
        print("You dropped less than 2 files on top of the program")
        input("Press Enter to continue...")
        sys.exit()

    if len(sys.argv) > 3:
        print("Usage: python main.py <file1> <file2>")
        print("You dropped more than 2 files on top of the program")
        input("Press Enter to continue...")
        sys.exit()

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if not os.path.isfile(file1):
        print(f"File {file1} not found")
        input("Press Enter to continue...")
        sys.exit()

    if not os.path.isfile(file2):
        print(f"File {file2} not found")
        input("Press Enter to continue...")
        sys.exit()

    print(f"Comparing {file1} and {file2}")
    comparer.compare(file1, file2)

    input("Press Enter to continue...")
    sys.exit()

if __name__ == '__main__':
    main()
