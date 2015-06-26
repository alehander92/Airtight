def sum(n: Integer) -> Integer:
    '''sum of the numbers from 0 to n inclusively'''
    result = 0
    for i in range(0, n + 1):
        result += i
    return result

print(sum(2000))
