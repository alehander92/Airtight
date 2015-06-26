def sum_while(n: Integer) -> Integer:
    result, i = 0, 0
    while i < n:
        i += 1
        result += i
    return result

print(sum_while(2000))
