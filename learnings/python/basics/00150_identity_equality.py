
print('\nTalking on variables\' compatision drops down with Equality "==" vs. Identity "is"')
print('Identity always leads to equality i.e. where "is" True, then "==" also True')
print('But NOT vice versa')


print('\nThere is no difference for int, str, bytes, bool, none and tuples')
i, j = 5, 5
print(f'{i} is {j} -', i is j)

str1, str2 = 'abc', 'abc'
print(f'{str1} is {str2} -', str1 is str2)

bstr1, bstr2 = b'abc', b'abc'
print(f'{bstr1} is {bstr2} -', bstr1 is bstr2)

bool1, bool2 = False, False
print(f'{bool1} is {bool2} -', bool1 is bool2)

none1, none2 = None, None
print(f'{none1} is {none2} -', none1 is none2)

tup1, tup2 = (1, 'a'), (1, 'a')
print(f'{tup1} is {tup2} -', tup1 is tup2)
print('We\'d not be ==/is for floats and complex because of floating point nature')


print('\nIf you think that difference will appear only on Mutable objects, it is WRONG.')
print('Tricks start with ranges. "is" result depends on how we assign value to variable')
i, j = range(5), range(5)
print('If created independently as i, j = range(5), range(5) are equal of course, but not identical')
print(f'{i} == {j} - ', i == j)
print(f'{i} is {j} - ', i is j)
print('But if created as assignment\ni = range(5)\nj = i')
j = i
print(f'{i} == {j} - ', i == j)
print(f'{i} is {j} - ', i is j)

print('\nOther immutable objects behave same way. Assigned independently, they equal but not identical.')
i, j = frozenset({1, 'a'}), frozenset({1, 'a'})
print(f'{i} == {j} - ', i == j)
print(f'{i} is {j} - ', i is j)


print('\nAll Mutable objects behave similarly. The difference comes natually with immutability:')
print('After object modificiation, all idential objects remain pointing to it. I.e. "is" remains!')

print('Sets:')
set1 = {1, 'a'}
set2 = set1
print(f'{set1} is {set2} - ', set1 is set2)
set2.add('bb')
print(f'{set1} is {set2} - ', set1 is set2)

print('Lists:')
list1 = [1, 'a']
list2 = list1
print(f'{list1} is {list2} - ', list1 is list2)
list2.append('bb')
print(f'{list1} is {list2} - ', list1 is list2)

print('Dicts:')
dict1 = {'1': 'a'}
dict2 = dict1
print(f'{dict1} is {dict2} - ', dict1 is dict2)
dict2['2'] = 'bb'
print(f'{dict1} is {dict2} - ', dict1 is dict2)

print('Bytearrays:')
bytearray1 = bytearray(2)
bytearray2 = bytearray1
print(f'{bytearray1} is {bytearray2} - ', bytearray1 is bytearray2)
bytearray2.append(0xff)
print(f'{bytearray1} is {bytearray2} - ', bytearray1 is bytearray2)
