import math
import sys
import time
import multiprocessing

from concurrent.futures import ThreadPoolExecutor
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
    for weight in cnt_different_by_weight.keys():
        x.append(weight)
        y.append(cnt_different_by_weight[weight])
    pairs = []
    for i in range(len(x)):
        pairs.append((x[i], y[i]))
    pairs.sort()
    file_output_name = 'output.txt'
    if len(sys.argv) >= 2:
        file_output_name = sys.argv[2]
    with open(file_output_name, 'w') as file:
        lastWeight = 0
        i = 0
        while i < len(pairs):
            if pairs[i][0] == lastWeight:
                print(pairs[i][0], pairs[i][1], file=file)
                i += 1
            else:
                print(lastWeight, 0, file=file)
            lastWeight += 1
    print('Имя файла', file_output_name)


def evaluate_mask(N, K, A, mask):
    res = '0' * N
    for bit in range(K):
        if ((mask >> bit) & 1):
            res = xor(res, A[bit])
    weight = res.count('1')
    lock.acquire()
    if weight not in cnt_different_by_weight:
        cnt_different_by_weight[weight] = 0
    cnt_different_by_weight[weight] += 1
    lock.release()
    return None


def find_all(A):
    N = len(A[0])
    K = len(A)
    with ThreadPoolExecutor(multiprocessing.cpu_count()) as executor:
        for mask in range(2 ** K):
            executor.submit(evaluate_mask, N, K, A, mask)
    build_graphic()
    return cnt_different_by_weight


def main():
    print('Введите название входного файла')
    file_name = 'input.txt'
    if len(sys.argv) > 2:
        file_name = sys.argv[1]
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
    print("--- %s seconds ---" % (time.time() - start_time), file=sys.stderr)
