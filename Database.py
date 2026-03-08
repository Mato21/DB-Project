"""
Simple persistent key-value database.

Supports the following commands:
SET <key> <value>
GET <key>
EXIT

Data is persisted in a log file (data.db).
"""
import sys
import os

DB_FILE = 'data.db'

def get_value_from_memory(stored_values: list, input_line: str) -> None:
    """Searches for the key in the list of stored values and prints the corresponding value if found. If the key is not found, it does not print anything."""
    parts = input_line.split()

    if len(parts) < 2:
        print('ERROR')
        return

    key = parts[1]
    for pair in stored_values:
        if pair[0] == key:
            print(pair[1])
            return

    
def set_value_into_memory(stored_values: list, input_line: str) -> None:
    """Appends key-value pair in the list within the memory and writes the pair to the data.db file. If the key already exists, it updates the value in memory and appends the new pair to the file."""
    parts = input_line[4:].split(' ', 1)

    if len(parts) < 2:
        print('ERROR')
        return

    key = parts[0]
    value = parts[1]
    found = False
    for pair in stored_values:
        if pair[0] == key:
            pair[1] = value
            found = True
            break
    if not found:
        stored_values.append([key, value])
    with open(DB_FILE, 'a') as f:
        f.write(f'SET {key} {value}\n')
        f.flush()
        os.fsync(f.fileno())
    print('OK')

def load_database() -> list:
    """This function loads the data from the data.db file into memory if it exists"""
    stored_values = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                for input_line in f:
                    line = input_line.strip()
                    if line.startswith('SET '):
                        key, value = line[4:].split(' ', 1)
                        found = False
                        for pair in stored_values:
                            if pair[0] == key:
                                pair[1] = value
                                found = True
                                break
                        if not found:
                            stored_values.append([key, value])  
        except OSError:
            print('ERROR')
    return stored_values

def main() -> None:
    """main function that checks for existing data file, loads it into memory, and processes commands until 'EXIT' is read"""
    stored = load_database()            
    #reads commands from stdin until 'EXIT' is read
    for line in sys.stdin:
        line = line.strip()

        if line == 'EXIT':
            break
        elif line.startswith('SET '):
            set_value_into_memory(stored, line)
        elif line.startswith('GET '):
            get_value_from_memory(stored, line)
        else:
            print('ERROR')

        sys.stdout.flush()

if __name__ == '__main__':
    main()