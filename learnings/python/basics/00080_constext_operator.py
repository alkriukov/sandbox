file1 = open('00010_hello.py', 'r')
file_contents = file1.read()
file1.close()
print(file_contents)

with open('00010_hello.py', 'r') as file2:
    file_contents = file2.read()
    print(file_contents)
