#include <iostream>
#include <string>
using namespace std;

int main()
{
    string flag = "flag{never_keep_secrets_in_code}";
    string correct_pass = "I_Feel_Lucky_Today";
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