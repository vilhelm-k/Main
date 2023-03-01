from hashtable import Hashtable

def main():
    hashtable = Hashtable(100)

    with open('DD1320/Lab7/test.txt') as f:
        for line in f:
            line = line.strip()
            key, *value = line.split()
            if key == '#':
                break
            elif len(value) != 0:
                hashtable.store(key, value[0])
            else:
                try:
                    value = hashtable.search(key)
                    print(value)
                except KeyError:
                    print('None')

if __name__ == "__main__":
    main()