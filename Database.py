import sys
import os

#gets the value of the pair from the memory and prnts it, if not found prints NULL
def get_value(store, line):
    parts = line.split()
    key = parts[1]
    for pair in store:
        if pair[0] == key:
            print(pair[1])
            break

    
    sys.stdout.flush()
#sets the pairs within the memory and appends to datt.db file
def set_value(store, line):
    parts = line.split(' ', 2)
    key = parts[1]
    value = parts[2]
    found = False
    for pair in store:
        if pair[0] == key:
            pair[1] = value
            found = True
            break

    if not found:
        store.append([key, value])
    with open('data.db', 'a') as f:
        f.write(f'SET {key} {value}\n')
        f.flush()
        os.fsync(f.fileno())
    print('OK')
    sys.stdout.flush()    


def main():
    store = []
    #checks existing data file and loads it into memory
    if os.path.exists('data.db'):
        with open('data.db', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('SET '):
                    key, value = line[4:].split(' ', 1)
                    found = False
                    for pair in store:
                        if pair[0] == key:
                            pair[1] = value
                            found = True
                            break
                    if not found:
                        store.append([key, value])               
    #reads commands from stdin until 'EXIT' is read
    for line in sys.stdin:
        line = line.strip()
        if line == 'EXIT':
            break
        elif line.startswith('SET '):
            set_value(store, line)
        elif line.startswith('GET '):
            get_value(store, line)
        else:
            print('ERROR')
            sys.stdout.flush()


if __name__ == '__main__':
    main()