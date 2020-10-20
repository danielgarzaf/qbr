#!/usr/bin/env python3

def reverse_nums(nums):
    reversed_nums = ''
    for i in range(len(nums) - 1, -1, -1):
        reversed_nums += nums[i]
    return reversed_nums

def wrap_nums(nums):
    return nums[0:3] + nums[4] + nums[7] + nums[6] + nums[5] + nums[3]



scramble = ''
with open ("scramble.txt", "r") as f:
    scramble = f.read()

solve = ''
with open("solve.txt", "r") as f:
    solve = f.read()

scramble_nums = ''
for letter in scramble:
    if letter == "U":
        scramble_nums += '0'
    elif letter == "B":
        scramble_nums += '1'
    elif letter == "R":
        scramble_nums += '2'
    elif letter == "F":
        scramble_nums += '3'
    elif letter == "L":
        scramble_nums += '4'
    elif letter == "D":
        scramble_nums += '5'

scramble_nums_parsed = []
for i in range(0, 54, 9):
    scramble_nums_parsed.append(scramble_nums[i:i+9])

white_nums = scramble_nums_parsed[0]
red_nums = scramble_nums_parsed[1]
green_nums = scramble_nums_parsed[2]
yellow_nums = scramble_nums_parsed[3]
orange_nums = scramble_nums_parsed[4]
blue_nums = scramble_nums_parsed[5] 

scramble_nums_parsed[1] = blue_nums
scramble_nums_parsed[2] = red_nums
scramble_nums_parsed[3] = green_nums
scramble_nums_parsed[5] = yellow_nums

print(scramble_nums_parsed)
for i, nums in enumerate(scramble_nums_parsed):
    scramble_nums_parsed[i] = reverse_nums(nums)
print(scramble_nums_parsed) 
for i, nums in enumerate(scramble_nums_parsed):
    scramble_nums_parsed[i] = nums[0:4] + nums[5:]
print(scramble_nums_parsed)
for i, nums in enumerate(scramble_nums_parsed):
    scramble_nums_parsed[i] = wrap_nums(nums)
print(scramble_nums_parsed)

i = 0
print("{int[48]}")
for face_nums in scramble_nums_parsed:
    for num in face_nums:
        print(f"\t[{i}]: {num}")
        i += 1


    
