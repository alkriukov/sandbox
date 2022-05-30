title = 'This script is about built-in plain data types'

print(-5, type(-5), hash(-5))
print(3.14, type(3.14), hash(3.14))
print(1+1j, type(1+1j), hash(1+1j))

print('Hello world', type('Hello world'), hash('Hello world')) # str is immutable object
print(b'Hello', type(b'Hello'), hash(b'Hello')) # bytes is immutable object. E.g. you get bytes with output from invoked process like output = subprocess.check_output(...)

print(True, type(True), hash(True))
print(None, type(None), hash(None))
