states = [line.strip() for line in open('states.txt')]

nums = [n for n in range(1, 52)]

ids = dict(zip(nums, states))

print ids




