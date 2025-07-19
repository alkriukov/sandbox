try:
    a = 1 / 0
except ZeroDivisionError as e:
    print('Exception handled:', type(e), e, '\n')

try:
    try:
        print('try-except can be nested')
        raise AttributeError()
    except AttributeError:
        print('Handled inner exception')
        raise Exception()
except Exception as e:
    print('Handled raised exception in outer except\n')

try:
    raise AttributeError()
except AttributeError as e:
    print('Start specific exceptions handling.\nNext except blocks usually handle more generic exceptions', type(e), e, '\n')
except Exception as e:
    pass

try:
    print('Full block is try-except-else-finally')
except Exception:
    pass
else:
    print('else block executed if NO exception occurred in try section')
finally:
    print('finally block executes in any case')

