import math
import time
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from threading import Lock

lock = Lock()
cnt_different_by_weight = dict()


def xor(a, b):
    n = len(a)
    res = [''] * n
    for i in range(n):
        val = ((ord(a[i]) - ord('0')) ^ (ord(b[i]) - ord('0')))
        res[i] = chr(ord('0') + val)
    return ''.join(res)


def build_graphic():
    x = []
    y = []
    maxWeight = 0

    for weight in cnt_different_by_weight.keys():
        x.append(weight)
        y.append(len(cnt_different_by_weight[weight]))
        maxWeight = max(maxWeight, weight)
    plt.bar(x, y)
    xint = range(min(x), math.ceil(max(x)) + 1)
    yint = range(min(y), math.ceil(max(y)) + 1)
    plt.xticks(xint)
    plt.yticks(yint)
    plt.xlabel('вес')
    plt.ylabel('количество различных векторов')
    pairs = []
    for i in range(len(x)):
        pairs.append((x[i], y[i]))
    pairs.sort()
    file_output_name = 'output.txt'
    with open(file_output_name, 'w') as file:
        for i in pairs:
            print(i[0], i[1], file=file)
    print('Имя файла', file_output_name)
    plt.savefig('hist.png')
    plt.show()


def evaluate_mask(N, K, A, mask):
    res = ['0'] * N
    for bit in range(K):
        if ((mask >> bit) & 1):
            res = xor(res, A[bit])
    weight = res.count('1')
    lock.acquire()
    if weight not in cnt_different_by_weight:
        cnt_different_by_weight[weight] = set()
    cnt_different_by_weight[weight].add(''.join(res))
    lock.release()
    return None


def find_all(A):
    N = len(A[0])
    K = len(A)
    with ThreadPoolExecutor(25) as executor:
        for mask in range(2 ** K):
            executor.submit(evaluate_mask, N, K, A, mask)
            # evaluate_mask(N, K, A, mask)
    build_graphic()
    return cnt_different_by_weight


def main():
    print('Введите название входного файла')
    file_name = 'input.txt'
    with open(file_name, 'r') as file:
        lines = file.readlines()
        A = []
        for line in lines:
            A.append(line.strip())
    find_all(A)
    return 0


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))
