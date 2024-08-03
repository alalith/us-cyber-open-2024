#include<stdio.h>

int i = 0;
int fake_rand[] = {5,4,4,1,6,6,5,6,4,6};
int rand() {
	return fake_rand[i++]-1;
}
