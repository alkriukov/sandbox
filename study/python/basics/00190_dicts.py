dict1 = {'a': 1, 'b': 2}
dict1['c'] = 'dicts are mutable...'
print(dict1)
try:
    dict1.hash()
except AttributeError as e:
    print('... so dicts are not hashable\n')