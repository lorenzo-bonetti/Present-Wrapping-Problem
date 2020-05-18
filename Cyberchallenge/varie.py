n = 0
for i in range(2, 2021, 2):
    if i % 5 == 0 and i % 7 == 0:
        n += 1

print(((2020 - 2) / 2) - n)

v = [1, 2, 3, 2, 1]

result = True
for i in range(0, int(5/2)):
    print(i)
    if v[i] != v[5-i-1]:
        result = False

print(result)

tries = [4040, 4039, 2020, 4038]
means = []
for num in tries:
    sum = 0
    for i in range(num+1):
        sum += i
    print(sum)
    print(num)
    means.append(sum/num)

print(means)

for i in range(1, 101):
    if pow(i, 1/3) % 1 == 0:
        print(i)

print(pow(64, 1/3))

letters = [60, 120, 360]
times = [36, 24, 30, 42]

for t in times:
    tot = 0
    for let in letters:
        perc = t/let*100
        tot += perc
    print("In {} minutes, {:.2f}% of the project is done".format(t, perc))