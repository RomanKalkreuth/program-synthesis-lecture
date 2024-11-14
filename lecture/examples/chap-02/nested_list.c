/* ------------------------------------------------------------------- */
/* C implementation of a nested list to represent symbolic expressions */
/*                                                                     */
/* Introduction to Program Synthesis Lecture                           */
/*                                                                     */
/* Author: Roman Kalkreuth                                             */
/* ------------------------------------------------------------------- */

#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <stdbool.h> 

struct Node* create_list(char* symbols, int *x, bool init_head);
struct Node* create_node(char symbol);
void append_node(struct Node* tail, char symbol);
void nest_node(struct Node* node, struct Node* sublist);
void remove_list(struct Node *head);
void traverse(struct Node* head);


struct Node{
    char symbol;
    bool annotated; 
    struct Node* next; 
    struct Node* nesting; 
};

struct Node* create_list(char* symbols, int* x, bool init_head) {
    struct Node* head = NULL;
    struct Node* node_ptr = NULL;
    struct Node* subhead = NULL;

    if(init_head) {
        head = (struct Node*) malloc(sizeof(struct Node));
        head->annotated = false;
        node_ptr = head;
    }

    int n = strlen(symbols);

    while(*x < n) {
       char s = symbols[*x];
       if(s != ' ') {
            if( s == '(') {
                (*x)++;
                subhead = create_list(symbols, x, true);
                if(head == NULL) {
                    head = subhead;
                    node_ptr = head;
                } else {
                    nest_node(node_ptr, subhead);
                }
            } else if (s == ')') {
                break;
            } else {
                if(head->annotated == false) {
                    head->symbol = s;
                    head->annotated = true;
                }
                else {
                    append_node(node_ptr, s);
                    node_ptr = node_ptr->next; 
                }      
            }
        }
        (*x)++;
    }
    return head;
} 

struct Node* create_node(char symbol) {
    struct Node* node = (struct Node*) malloc(sizeof(struct Node));
    node->symbol = symbol;
    node->annotated = true; 
    node->next = NULL;
    return node;
}

void append_node(struct Node* tail, char symbol) {
    struct Node* node = create_node(symbol);
    tail->next = node;
}

void nest_node(struct Node* node, struct Node* sublist) {
    node->nesting = sublist;
}

void remove_list(struct Node *head) {
    struct Node* node_ptr = head;
    struct Node* tmp; 

    while (node_ptr != NULL) {
        if(node_ptr->nesting != NULL){
            remove_list(node_ptr->nesting);
        }
        tmp = node_ptr->next;
        free(node_ptr);
        node_ptr = tmp;
     }  
}

struct Node* tail(struct Node* head) {
    struct Node* node_ptr = head;
    while (node_ptr->next != NULL) {
        node_ptr = node_ptr->next;
     }   
    return node_ptr;
}

void traverse(struct Node* head) {
   struct Node* node_ptr = head;
    while (node_ptr != NULL) {
        if(node_ptr->nesting != NULL){
            traverse(node_ptr->nesting);
        }
        node_ptr = node_ptr->next;
     }   
}

int main(void) {
    char expr[] = "(*a (b+c))";
    int x = 0; 
    struct Node* head = create_list(expr, &x, false);
    remove_list(head);
}
