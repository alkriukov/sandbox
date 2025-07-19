import os

os.system('strings vault > strs_in_vault.txt')

with open('strs_in_vault.txt', 'r') as f:
    strs = f.read().split('\n')

for s in strs:
    os.system('echo ' + s + ' > pass.txt')
    os.system('./vault < pass.txt > out.txt')
    with open('out.txt', 'r') as fo:
        out = fo.read()
        if 'is not correct' not in out:
            print(s)
            print(out)

os.system('rm strs_in_vault.txt pass.txt out.txt')
