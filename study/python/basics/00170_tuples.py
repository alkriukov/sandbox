
tup1 = ('response_text', 200)
print(f'\nTuple is an ordered collection: {tup1} is {type(tup1)}')

print(f'You can get element by index. E.g. 2nd element is {tup1[1]}\n')

print('In contrary to lists, tuples are IMMUTABLE and HASHABLE:')
tup2 = ('another_response_text', 403)
third_tuple_object = tup1 + tup2
print(f'{third_tuple_object} hash is {hash(third_tuple_object)}\n')


for x in tup2:
    print(f'You can iterate thru tuples: {x}')
