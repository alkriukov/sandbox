i = 0
while i < 3:
    print(i)
    i += 1

iterable_object = range(3)
for i in iterable_object:
    for j in range(2):
        print('Inner cycle:', i, j)

for i in range(3):
    print(i, 'Pass does nothing. It is convenient to fill block, as python does not have {}')
    pass

for i in range(3):
    print(i, 'Continue switches immediately to next round of cycle')
    continue
    print('This will not be printed')

for i in range(3):
    print(i, 'Break ends entire cycle. Next i will not occur.')
    break
    print('Cycle ended with the first iteration')

for i in range(3):
    pass
    if i >= 3:
        break
else:
    print('for-break-else constuction: else occurs if cycle ended, and break never happend')

