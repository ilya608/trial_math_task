import math
import sys
import time


def code_gray(n):
    res = []
    for i in range(0, 1 << n):
        gray = i ^ (i >> 1)
        res.append(int("{0:0{1}b}".format(gray, n)))
    return res


def xor(a, b):
    n = len(a)
    res = [''] * n
    for i in range(n):
        val = ((ord(a[i]) - ord('0')) ^ (ord(b[i]) - ord('0')))
        res[i] = chr(ord('0') + val)
    return ''.join(res)


def build_graphic(cnt_different_by_weight):
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


def find_all(A):
    N = len(A[0])
    K = len(A)
    for i in range(len(A)):
        A[i] = int(A[i], base=2)
    cnt_different_by_weight = dict()
    masks = code_gray(K)
    res = 0
    for i in range(2 ** K):
        if i == 0:
            dif = 0
        else:
            dif = (masks[i] ^ masks[i - 1])
        for bit in range(K):
            cur_bit = ((dif >> bit) & 1)
            if cur_bit != 0:
                res ^= A[bit]
        weight = bin(res)[2:].count('1')
        if weight not in cnt_different_by_weight:
            cnt_different_by_weight[weight] = 0
        cnt_different_by_weight[weight] += 1
    build_graphic(cnt_different_by_weight)
    return cnt_different_by_weight


def main():
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
