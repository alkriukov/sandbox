
list1 = ['Let\'s', 'start', 'with', 'list']
print(' '.join(list1))

list2 = ['It is Ok to have', 2, 'or more data types in the list.', 'But don\'t use join then']

list3 = [1, 2, -3, 5]
list3.sort()
print(list3, type(list3))

list4 = list3
if list3 is list4:
    print('= operator makes actually same list object')
list3.append(7)

if list3 == list4 and list3 is list4:
    print('Lists are mutable objects...')
try:
    list3.hash()
except AttributeError as e:
    print('... so lists are not hashable')

list5 = list3.copy()
if list5 == list3 and list5 is not list3:
    print('Copying list makes different object')


tup1 = (1, 'a', True)
print(tup1, type(tup1), hash(tup1))


range1 = range(1, 5, 2)
print(range1, type(range1), hash(range1))


set1 = {1, 'a', True}
set1.add('sets are mutable...')
print(set1, type(set1))
try:
    set1.hash()
except AttributeError as e:
    print('... so sets are not hashable')

fset1 = frozenset(set1)
try:
    fset1.add('something')
except AttributeError as e:
    print('In contrary to sets, frozen sets are immutable')
try:
    hash(fset1)
    print('So, frozen sets are hashable')
except AttributeError as e:
    print('Frozen sets are not hashable')






dict1 = {'a': 1, 'b': 2}
dict1['c'] = 'dicts are mutable...'
print(dict1)
try:
    dict1.hash()
except AttributeError as e:
    print('... so dicts are not hashable')

print(type(bytearray(5))) # Mutable
print(type(memoryview(bytes(5)))) # In contrary to raw bytes/str, memoryview allows slicing without underlying data copy. Very memory-efficient & fast in large data volumes

