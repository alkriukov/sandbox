true_var = True
false_int = 0
false_str = ''
false_null = None
false_list = []

if True:
    print('True is True')


if false_int:
    pass
else:
    print('0 is False')


if false_str:
    print('Empty string is True')
elif false_null:
    print('Empty string is False, but None is True')
elif not false_list:
    print('Empty string is False, None is False, and [] is also False')
else:
    print('Empty string is False, None is False, but [] is True')


if True or False:
    print('True or False is True')

if not (True and False):
    print('True and False is False')
