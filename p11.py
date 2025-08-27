if __name__ == '__main__':
    x = int(input())
    y = int(input())
    z = int(input())
    n = int(input())

    # Create a list of all possible coordinates [i, j, k]
    # where i, j, k are within their respective ranges,
    # and the sum i + j + k is not equal to n.
    result = [[i, j, k] for i in range(x + 1) for j in range(y + 1) for k in range(z + 1) if i + j + k != n]

    print(result)