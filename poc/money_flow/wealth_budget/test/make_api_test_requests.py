import requests, json

artif = {}

n_passed = 0
n_failed = 0

def testRequest(expected, method, url, heads, body, test_id):
    test_passed = False
    resp = 'FAIL: Request Was Not Run'
    try:
        match method.upper():
            case 'GET':
                resp = requests.get(url, headers=heads, json=body).text
            case 'POST':
                resp = requests.post(url, headers=heads, json=body).text
            case 'PUT':
                resp = requests.put(url, headers=heads, json=body).text
            case 'DELETE':
                resp = requests.delete(url, headers=heads, json=body).text
            case 'OPTIONS':
                resp = requests.options(url, headers=heads, json=body).text
   
    except requests.exceptions.ConnectionError as e:
        resp = 'FAIL: ConnectionError ' + str(type(e))
    except Exception as e:
        resp = 'FAIL: ' + str(type(e))
    if expected in resp:
        result = '   PASS '
        test_report = ' '.join([result, '{0: <7}'.format(method), 
                                    '{0: <43}'.format(url),
                                    '{0: <22}'.format(json.dumps(body)[:20]),
                                    '{0: <22}'.format(resp[:30])])
        test_passed = True
    else:
        result = '!!!FAIL!'
        test_report = ' '.join([result, '{0: <7}'.format(method), 
                                        '{0: <43}'.format(url),
                                        json.dumps(body),
                                        resp])
    artif[test_id] = json.loads(resp)
    return test_passed, test_report

def run_test(t):
    global n_passed
    global n_failed
    if 'test_id' not in t.keys():
        t['test_id'] = 'test'
    test_passed, report = testRequest(t['e'], t['m'], t['u'], t['h'], t['b'], t['test_id'])
    if test_passed:
        n_passed += 1
    else:
        n_failed += 1
    print(report)

def summary():
    print('\n  PASSED:', n_passed, '\n  FAILED:', n_failed, '\n')
