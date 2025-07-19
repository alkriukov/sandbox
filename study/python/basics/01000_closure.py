def key_custodian(secret_key):
    key = secret_key
    def check_key(key):
        return key == secret_key
    return check_key

app_key_checker = key_custodian('sdlfkj2039409gu0UF)IW')

key1 = 'sdlfkj2039409gu0UF)IW'
key2 = 'sdlfkj203923oi09vn)IW'
print(app_key_checker(key1))
print(app_key_checker(key2))
