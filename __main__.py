import sys
from .runtime import Boomlang

def main():
    if len(sys.argv) != 2:
        print("Usage: Boomlang <filename.boom>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, "r", encoding="UTF-8") as file:
        code = file.read()

    interpreter = Boomlang()
    interpreter.compile(code)

if __name__ == "__main__":
    main()