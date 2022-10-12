class MyClass:
    pass


def get_arg(myclass: MyClass) -> MyClass:
    print(type(myclass))
    return myclass

a = MyClass()
b = get_arg(a)
