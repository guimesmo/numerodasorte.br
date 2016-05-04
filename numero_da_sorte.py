import random

def numero_da_sorte():
    l = list(range(1, 61))
    random.shuffle(l)
    result = l[:6]
    result.sort()
    return "-".join([str(i).zfill(2) for i in result])

if __name__ == '__main__':
    print(numero_da_sorte())

