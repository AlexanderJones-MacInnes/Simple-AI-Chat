#include <iostream>
#include <windows.h>
#include <stdlib.h>

using namespace std;

int main(int argc, char* argv[])
{
    int x, y;
    if(argc >= 3)
    {
        x = atoi(argv[1]);
        y = atoi(argv[2]);
    }
    SetCursorPos(x,y);
    return 0;
}
