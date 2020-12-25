def xor(a, b):
    return bool((not a and b) or (not b and a)) and ((not a and b) or (not b and a))


print("1, 1: ", xor(1, 1))
print("1, 0: ", xor(1, 0))
print("0, 1: ", xor(0, 1))
print("0, 0: ", xor(0, 0))
