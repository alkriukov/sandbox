#include <iostream>
#include <string>
using namespace std;

int main()
{
    string flag = "n3v3r_k33p_s3cr3ts_1n_c0d3";
    string correct_pass = "iFeelLuckyT0d@y";
    string attempt_pass;
    cout << "The password is 10+ symbols long with Capital and lowercase symbols,\nditits and special symbols!\nGood luck guessing it:\n";
    cin >> attempt_pass;
    if (attempt_pass == correct_pass) {
        cout << "flag{" << flag << "}\n";
    }
    else {
        cout << "The password is not correct. No wonder why! Loser.." << endl;
    }
    return 0;
}
