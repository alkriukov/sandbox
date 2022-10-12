def print_hello():
    print('Hello world')

def print_greeting(name):
    print(f'Hello {name}')

def greeting(name: str) -> str:
    return f'Hello {name}'

print_hello()
print(print_hello)

print_greeting('Alexey')
print(print_greeting)

print(greeting('Alexey'))
print(greeting)
