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
