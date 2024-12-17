/* ------------------------------------------------------------------------ */
/* C99 implementation of a adjacency matrix                                 */
/*                                                                          */
/* Introduction to Program Synthesis Lecture (Chapter 02 - Foundations)     */
/*                                                                          */
/* Author: Roman Kalkreuth                                                  */
/* ------------------------------------------------------------------------ */

#include <stdio.h>
#include <stdlib.h> 
#include <stdbool.h>
#include <string.h> 

#define N 10

int** create_matrix(int n);
void remove_matrix(int** m, int n);
void add_edge(int** m, int u, int v);
void remove_edge(int** m, int u, int v);
 
int** create_matrix(int n) {
    int** m = malloc(n*sizeof(int*));
    for(int i = 0; i < n; i++) {
        m[i] = malloc(n*sizeof(int));
        memset(m[i], 0, n*sizeof(*m[i]));
    }
    return m;
}

void remove_matrix(int** m, int n) {
    for(int i = 0; i < n; i++) {
        free(m[i]);
    }    
}

void add_edge(int** m, int u, int v){
    m[u][v] =  1;
    m[v][u] =  1; 
}

void remove_edge(int** m, int u, int v){
    m[u][v] =  0;
    m[v][u] =  0;
}

int main(void) {
    int** m = create_matrix(N);
    remove_matrix(m, N);
}