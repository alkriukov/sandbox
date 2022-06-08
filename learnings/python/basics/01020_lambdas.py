
print('\nLambda is an assigned or anonymous function in Python')

print('Assigned example name = lambda arg1, arg2, argN : return expression')
multiply = lambda a, b : a * b
print(multiply(2, 10))

def amplifyWrapper(koeff):
    return lambda a : a * koeff
amplifyX10 = amplifyWrapper(10)
print(amplifyX10(2))

