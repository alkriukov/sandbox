import os, sys

name = sys.argv[1]
greeting = 'Hi ' + name

print(greeting)
os.system('echo '+ greeting)
