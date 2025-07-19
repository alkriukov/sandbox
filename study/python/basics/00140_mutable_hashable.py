
print('\nFundamental variables characreristics is (Im)MUTABLE and (Non)HASHABLE')
print('Let\'s see.')

plain_vars =   ['Hello', -5, 2.7271, 1+1j, b'Hello', True, None]
collect_vars = [[1, 'list'], (1, 'tuple'), range(2),
    {1, 'set'}, frozenset({1, 'set'}),
    {'a': 'dictionary'}, bytearray(3)]

all_my_vars = plain_vars + collect_vars
hashable_types_are_immutable = True

for my_var in all_my_vars:
    var_report = '{:>27}'.format(f'{my_var}') + '    {:<20}'.format(f'{type(my_var)}')
    try:
        var_hash = hash(my_var)
        var_report += '     Hashable'
    except TypeError as e:
        var_report += ' Non-Hashable'
    if hashable_types_are_immutable:
        if var_report[-12:] == '    Hashable':
            var_report += '   Immutable'
        else:
            var_report += '     Mutable?'
    print(var_report)

print('\nSo, let\'s check if Lists, Sets, Dicts and ByteArrays indeed Mutable')
list1 = ['1', '2']
list2 = list1
list2.append('3')
if '3' in list1:
    print(f'Correct! {type(list1)}      - Mutable')

set1 = {'1', '2'}
set2 = set1
set2.add('3')
if '3' in set1:
    print(f'Correct! {type(set1)}       - Mutable')

dict1 = {'1': 1, '2': 2}
dict2 = dict1
dict2['3'] = 3
if '3' in dict1.keys():
    print(f'Correct! {type(dict1)}      - Mutable')

bytearray1 = bytearray(5)
bytearray2 = bytearray1
bytearray1.append(0xff)
if 0xff in bytearray1:
    print(f'Correct! {type(bytearray1)} - Mutable')


print('\nIn contrary, even being able to read item in tuple or string e.g. tup[i], st[i], you can\'t assign value to it:')
tup1 = ('a', 1)
try:
    tup1[0] = 'b'
except TypeError as e:
    print('Cannot modify tuple ', type(e), e)
str1 = 'abc'
try:
    str1[0] = 'b'
except TypeError as e:
    print('Cannot modify string', type(e), e)


print('\nReasonable question: why we\'re saying about mutable/hashable Variables, not Types?')
print('Actually one can say immutable/hashable for non-collection types.')
print('But for collections, it really depends on what it contains!')
print('If a collection e.g. tuple has mutable object e.g. list - it won\'t be hashable')
some_tuple = (1, [2])
try:
    print(type(some_tuple), hash(some_tuple))
except TypeError as e:
    print(e)

print('\nNote that Hashable elements are crucial for Sets (have only unique values) and Dicts keys')
try:
    set3 = {list1}
except TypeError as e:
    print('Set rejects List element:', type(e), e)
try:
    dict3 = {list1: 'aa'}
except TypeError as e:
    print('Dict rejects List key:', type(e), e)
    print({'aa': list1}, ' list values are Ok for Dicts')
