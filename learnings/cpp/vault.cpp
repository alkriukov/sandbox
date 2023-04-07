#include <iostream>
#include <string>
using namespace std;

int main()
{
    string password = "hello_password";
    string flag = "flag{sfli23i23fpfo2}";
    string attempt_p;
    cout << password << endl;
    cin >> attempt_p;
    if (attempt_p == password) {
        cout << flag;
    }
    else {
        cout << "The password is not correct" << endl;
    }
    return 0;
}