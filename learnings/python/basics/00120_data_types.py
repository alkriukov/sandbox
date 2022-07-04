
some_str = '\nBuilt-in plain types'
print(some_str, type(some_str))

some_integer = -5
print(some_integer, type(some_integer))
ok_to_convert_str_to_int = int('30')
print(ok_to_convert_str_to_int, type(ok_to_convert_str_to_int))

some_float = 3.14159
print(some_float, type(some_float))
ok_to_convert_to_float = float(-1000)
print(ok_to_convert_to_float, type(ok_to_convert_to_float))

some_complex = 1+1j
print(some_complex, type(some_complex))

some_bytes = b'Hello World'
print(some_bytes, type(some_bytes)) # bytes is immutable object. E.g. you get bytes with output from invoked process like output = subprocess.check_output(...)

some_bool = True
print(some_bool, type(some_bool))

none_variable = None
print(none_variable, type(none_variable))


