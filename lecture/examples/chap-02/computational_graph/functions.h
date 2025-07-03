#ifndef LIST_H
#define LIST_H

int add(int* op1, int* op2);
int sub(int* op1, int* op2);
int mul(int* op1, int* op2);
int pdiv(int* op1, int* op2);

int add(int* op1, int* op2) {
    return *op1 + *op2;
}

int sub(int* op1, int* op2) {
    return *op1 - *op2;
}

int mul(int* op1, int* op2) {
    return *op1 * *op2;
}

int pdiv(int* op1, int* op2) {
    if(*op2 == 0) {
        return 1;
    }
    return *op1 / *op2; 
} 

#endif


