title = 'Variables are declared via = operator.'
print(title)

a, b = 'Multiple delcarations', 'are Ok'
print(a)
print(b)


print('\nEach variables "lives" in own scope. It can be:')
print(' * block scope (local and enclosed namespaces)\n * module scope (global namespace)\n * built-in (scope & namespace)')

print('Built-in variables are True, False, None, NotImplemented, Ellipsis, __debug__')
var_from_built_in_scope = False

some_var = 'Global scope variable - can be accessed from any part of the program'
def outer_f():
    some_var = '\nBy default, Outer scope variable - can be accessed within its block'

    def inner_f0():
        print(some_var)
    inner_f0()

    def inner_f1():
        nonlocal some_var
        some_var = 'Reassigned Outer scope variable - use nonlocal keyword for this'
    inner_f1()
    print(some_var)

    def inner_f2():
        global some_var
        print(some_var)
        some_var = 'Reassigned Global scope variable - use global keyword for scope resolution'
    inner_f2()

outer_f()
print(some_var)
