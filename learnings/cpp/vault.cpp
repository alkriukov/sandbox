#include <iostream>
#include <string>
using namespace std;

int main()
{
    string flag = "flag{sfli23i23fpfo2}";
    string correct_pass = "hello_password";
    string attempt_pass;
    cout << "Enter password" << endl;
    cin >> attempt_pass;
    if (attempt_pass == correct_pass) {
        cout << flag << endl;
    }
    else {
        cout << "The password is not correct" << endl;
    }
    return 0;
}
