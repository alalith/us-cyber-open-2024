#include<stdio.h>

int i = 0;
int fake_rand[] = {8,8,3,8,7,4,4,3,8,8,8,8,8,2,5,2};

int rand() {
	return fake_rand[i++]-1;
}
