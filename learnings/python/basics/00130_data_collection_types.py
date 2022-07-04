
list1 = ['\nPython ', 'collection ', 'types ', 'are\n', ' * Lists:  ', ]
print(''.join(list1) + str(list1))

tup1 = (1, 'a', True)
print(f' * Tuples: {tup1}')

range1 = range(1, 5, 2)
print(' * Ranges:', range1)

set1 = {1, 'a', True}
print(' * Sets:', set1)

fset1 = frozenset(set1)
print(' * Frozen Sets:', fset1)

dict1 = {'a': 1, 'b': 2}
print(' * Dictionaries:', dict1)

bar1 = bytearray(5)
bar1.append(0xff)
bar1[0] = 255
print(' * Bytearrays:', bar1)


print(' * Memoryview can be made e.g. for bytes and bytearrays')
print('   But in contrary to raw bytes/bytearrays, memoryviews allow slicing without underlying data copy.')
print('   Very memory-efficient & fast in large data volumes')
bt1 = bytes(5)
mem1 = memoryview(bt1)
print('   ', mem1, type(mem1), 'over', type(bt1), hash(bt1))
mem2 = memoryview(bar1)
print('   ', mem2, type(mem2), 'over', type(bar1))


print('\nSlicing is a powerfull tool to work with sub-collections.\nInstead of poining to single element [i], it has [start_index_inclusive:end_index_non_inclusive:step]')
print([0, 1, 2, 3, 4,], '> [1:4] >', [0, 1, 2, 3, 4,][1:4])
print((0, 1, 2, 3, 4, 5, 6), '> [1::2] >', (0, 1, 2, 3, 4, 5, 6)[1::2])
print('"012345678"', '> [1:-1:-1] >', '012345678'[-1:1:-2])
