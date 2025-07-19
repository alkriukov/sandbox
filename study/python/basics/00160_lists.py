from copy import deepcopy

list1 = ['Let\'s', 'start', 'with', 'list', ]
print(' '.join(list1))

list2 = ['It is Ok to have', 2, 'or more data types in the list.', 'But don\'t use join then']
print(list2)

print('Common list operations are appending, extending, element-wise work')
list3 = [1, 2, -3, 5]
list3.append(8)
list3.extend([3, -2, 11, 5, 12, 4])
last_element = list3.pop()
index_of_el = list3.index(3)
list3.remove(12)
list3.insert(4, 19)
print(list3)
list3.sort()
print(list3)



print('\nList comprehension is a constuction [expression] e.g.')
print('List generators:')
generated_list1 = [i + 1 for i in range(5)]
print('[i + 1 for i in range(5)] gives', generated_list1)
generated_list2 = [i * i for i in range(1, 8) if i % 2 == 1]
print('[i * i for i in range(1, 8) if i % 2 == 1] gives', generated_list2)

print('Parallel iterators:')
list4 = [0, 1, 2]
list5 = [3, 4, 5]
list6 = [6, 7, 8]
list7 = [x * y * z for (x, y, z) in zip(list4, list5, list6)]
print(list7)

print('Flattening 2D list with double "for" inside []:')
list_2d = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
list_flat = [x   for list_1d in list_2d   for x in list_1d]
print(list_flat)

nested_list = [1, 2, [1, 2]]
print('\nNested list', str(nested_list))
shallow_copy = nested_list.copy()
deep_copy = deepcopy(nested_list)

shallow_copy.append(3)
shallow_copy[2].append(4)
deep_copy.append(5)
deep_copy[2].append(6)

if nested_list is not shallow_copy and nested_list[2] is shallow_copy[2]:
    print('list.copy() makes a copy of initial list. But if it contains another list, it won\'t make a copy of it.')
    print('So when we modify nested mutable collection, it will affect all copies:')
    print(nested_list, shallow_copy)

if nested_list is not deep_copy and nested_list[2] is not deep_copy[2]:
    print('deepcopy makes a recursive copy of all list items also. So the changes are completely independent:')
    print(nested_list, deep_copy)

