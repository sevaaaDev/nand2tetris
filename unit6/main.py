# first pass add label to symbol table
# second pass evaluate command to binary


# for line in file:
    # label = parseLabel(line);
    # symbol.add(label);

# for line in file:
    # command = parse(line);
    # command.eval();

# command is class
# method eval()

import sys
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def toBinary(self, symbol: dict[str, int]) -> str:
        pass

def parse(line: str) -> Command:
    return None

def main():
    symbol_table: dict[str, int] = [] # TODO: fix this
    with open(sys.argv[1], 'r') as file:
        # TODO: figure out how to restart loop
        for line in file:
            command: Command = parse(line)
            print(command.toBinary(symbol_table))

if __name__ == "__main__":
    main()
