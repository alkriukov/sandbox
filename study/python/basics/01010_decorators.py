def lowercase_decorator(func):
    def wrapper(*args, **kwargs):
        print('applying lowercase ...')
        return str(func(*args, **kwargs)).lower()
    return wrapper

@lowercase_decorator
def hello():
    return 'Hello!'

@lowercase_decorator
def hello_name(name):
    return ''.join(['Hello ', str(name), '!'])

print(hello())
print(hello_name('Alexey'))



def error_handling(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e, 'Handled in decorator')
    return wrapper

def raise_error():
    raise Exception()

@error_handling
def raise_another_error():
    raise Exception()

try:
    raise_another_error()
except Exception as e:
    print('Handled on top-level')

try:
    raise_error()
except Exception as e:
    print(e, 'Handled on top-level')