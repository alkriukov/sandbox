def print_greeting(name: str) -> str:
    print('Hello', name)
    return 'Done'

print(print_greeting('Olga'))


def print_custom_greeting(name: str, msg: str = 'Hello') -> None:
    print(msg, name)

print_custom_greeting('Vlad')
print_custom_greeting('Max', msg='Hi')


def f_with_args_kwargs(*args: str, **kwargs) -> None:
    for position_arg in args:
        print(position_arg)
    for key, value in kwargs.items():
        print(key, value)

f_with_args_kwargs('Hello', msg='You are welcome')
f_with_args_kwargs('Hello', 'Alexey', msg='You are welcome', bye='Bye!')


def f_with_mandatory_and_optional_args(mandatory_positional_arg: str, *args, kw: str = 'Keyword agrument', **kwargs) -> None:
    print(mandatory_positional_arg)
    for position_arg in args:
        print(position_arg)
    print('kw', kw)
    for key, value in kwargs.items():
        print(key, value)

f_with_mandatory_and_optional_args('Hello', 'Alexey', kw='You are welcome', bye='Bye!')
