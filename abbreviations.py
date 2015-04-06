abbs = [line.strip() for line in open('abbr.txt')]

nums = [n for n in range(1, 52)]

abb_ids = dict(zip(nums, abbs))

print abbs

print abb_ids