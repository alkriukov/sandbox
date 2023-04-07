#include <iostream>
#include <string>
using namespace std;

int main()
{
    string flag = "flag{never_keep_secrets_in_code}";
    string correct_pass = "iFeelLuckyT0d@y";
    string attempt_pass;
    cout << "The password is 10+ symbols long with Capital and lowercase symbols,\nditits and special symbols!\nGood luck guessing it: " << endl;
    cin >> attempt_pass;
    if (attempt_pass == correct_pass) {
        cout << flag << endl;
    }
    else {
        cout << "The password is not correct" << endl;
    }
    return 0;
}
