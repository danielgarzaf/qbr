#!/usr/bin/env python3
import numpy as np

# parse each face values
def parse_nums(nums):
    scramble_parsed = []
    for i, num in enumerate(nums):
        if i % 9 == 0 and i != 0:
            scramble_parsed.append(nums[i - 9 : i])
        elif i == len(scramble) - 1:
            scramble_parsed.append(nums[i - 8 : i + 1])
    return scramble_parsed


scramble = ""
with open("txts/scramble.txt", "r") as f:
    scramble = f.read()

scramble_nums = ""
for idx, letter in enumerate(scramble):
    if letter == "U":
        scramble_nums += "0"
    elif letter == "B":
        scramble_nums += "1"
    elif letter == "R":
        scramble_nums += "2"
    elif letter == "F":
        scramble_nums += "3"
    elif letter == "L":
        scramble_nums += "4"
    elif letter == "D":
        scramble_nums += "5"
scramble = scramble_nums
# parse each face values
scramble_parsed = parse_nums(scramble)

# populate matrix
n = len(scramble_parsed[0])
rows = n // 3
cols = n // rows
scramble_matrix = np.zeros((len(scramble_parsed), rows, cols))
for index, nums in enumerate(scramble_parsed):
    for i in range(rows):
        for j in range(cols):
            scramble_matrix[index][i][j] = nums[i * cols + j]

# rotate matrixes accordingly
for i in range(len(scramble_matrix)):
    block = scramble_matrix[i]
    block[:] = np.rot90(block, 1).copy()
    if scramble_matrix[i][1][1] == 5:
        block[:] = np.rot90(block, 1).copy()
        block[:] = np.rot90(block, 1).copy()
    elif scramble_matrix[i][1][1] == 0:
        pass
    else:
        block[:] = np.rot90(block, 1).copy()

# prepare output var
res = ""
for i in range(len(scramble_matrix)):
    for j in range(len(scramble_matrix[i])):
        for k in range(len(scramble_matrix[i][j])):
            res += str(int(scramble_matrix[i][j][k]))
res = parse_nums(res)
res = [
    res[0],
    res[-1],
    res[1],
    res[2],
    res[-2],
    res[-3],
]

for i, nums in enumerate(res):
    res[i] = nums[:4] + nums[5:]

output = ""
for nums in res:
    output += nums[:3] + nums[4] + nums[-1] + nums[-2] + nums[-3] + nums[3]

i = 0
with open("txts/setState.txt", "w") as f:
    f.write("{int[48]}\n")
    for nums in output:
        for num in nums:
            text = f"    [{i}]: {num}\n"
            f.write(text)
            i += 1
