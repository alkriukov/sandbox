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
    print('So, frozen sets are hashable\n')
except AttributeError as e:
    print('Frozen sets are not hashable\n')