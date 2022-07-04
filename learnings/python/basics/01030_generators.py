def square_gen():
    i = 0
    max = 10
    while i < max:
        square = i * i
        i += 1
        yield square

squares = square_gen()
print(squares)

print(next(squares))
print(next(squares))
print(next(squares))
print(next(squares))

print()
for item in square_gen():
    print(item)
