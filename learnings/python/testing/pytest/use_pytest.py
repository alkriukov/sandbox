from attr import s
import os
import pytest
from pytest import approx

def add_fnc(a, b):
    return a + b

def f_should_raise_system_exit():
    raise SystemExit(1)


def test_add_fnc_int():
    assert add_fnc(3, 5) == 8

def test_add_fnc_float():
    assert (add_fnc(0.1, 0.2), add_fnc(0.1, -0.1)) == approx((0.3, 0.0))

@pytest.mark.timeout(10)
def test_f_system_exit():
    with pytest.raises(SystemExit):
        f_should_raise_system_exit()

def test_output(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"

def test_system_echo(capfd):
    os.system('echo hello')
    captured = capfd.readouterr()
    assert "hello" in captured.out

feature_not_developed = {'F12345': True}
@pytest.mark.xfail(condition=feature_not_developed['F12345'], reason='F12345 not ready')
def test_F12345():
    assert True

def test_needs_tmp_path(tmp_path, pytestconfig):
    fail_msg = str(tmp_path)
    if pytestconfig.getoption("verbose") > 0:
        fail_msg = 'Report: ' + fail_msg
    pytest.fail(str(fail_msg))

