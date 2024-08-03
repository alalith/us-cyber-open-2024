#include <iostream>
#include <string>
#include <cstdlib>

using namespace std;
    unsigned char hexArray1[] = {
        0xad, 0x75, 0xff, 0x83, 0xd5, 0xc0, 0x73, 0x16,
        0x2c, 0x2a, 0xf7, 0x2e, 0x7b, 0x45, 0xb4, 0x96,
        0xfb, 0x81, 0xa9, 0x7b, 0x69, 0x69
    };
        unsigned char hexArray2[] = {
        0xfe, 0x3c, 0xa9, 0xc1, 0x92, 0x92, 0x08, 0x6e, 
        0x1c, 0x58, 0xa8, 0x6c, 0x3b, 0x36, 0x85, 0xf5, 
        0x88, 0xde, 0xfb, 0x48, 0x1f, 0x14
    };
// Function to check if the input string is correct
bool checkString(const string& input) {
    if(input.size()==22) {
        for(int i=0;i<=22;i++) {
            char test = hexArray1[i]^hexArray2[i];
	    putc(test, stdout);
        }
    } else {
        return 0;
    }
    return 1;

}

int main() {
    cout << "Enter the correct flag to pass: ";

    string userInput;
    getline(cin, userInput);

    if (checkString(userInput)) {
        cout << "Correct!" << endl;
    } else {
        cout << "Sorry, the input is incorrect. Try again!" << endl;
    }

    return 0;
}
