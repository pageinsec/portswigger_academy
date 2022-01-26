import random
import string

strings = []
randos = []
inputs = input('How many strings should be generated? ')
i = int(inputs)
for x in range(0,i):
    length = int(input(f'Length of string {x}: '))
    strings.append(length)
for y in strings:
    k = ''.join(random.choice(string.ascii_letters) for k in range(y))
    randos.append(k)
    print(f'String of length {y}: {k}')


