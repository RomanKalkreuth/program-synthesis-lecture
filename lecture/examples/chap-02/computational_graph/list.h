#ifndef LIST_H
#define LIST_H

#include <stdlib.h> 
#include <stdbool.h> 
#include "graph.h"

struct Edge{
    struct FunctionNode* vertex;
    struct Edge* prev;
    struct Edge* next;
    int input_id;
};

struct Edge* create(struct FunctionNode* vertex, int input_id) {
    struct Edge* node = (struct Edge*) malloc(sizeof(struct Edge));
    node->vertex = vertex;
    node->input_id = input_id;
    node->next = NULL;
    node->prev = NULL;
    return node;
}

struct Edge* create(struct FunctionNode* vertex, int input_id);
struct Edge* tail(struct Edge* head);
void clear(struct Edge *head);
void append(struct FunctionNode* head, int (*function_ptr)(int,int), int id);
void remove(struct FunctionNode* head, int id);


void clear(struct Edge *head) {
    struct Edge* node_ptr = head->next;
    struct Edge* tmp; 

    while (node_ptr != NULL) {
        tmp = node_ptr->next;
        free(node_ptr);
        node_ptr = tmp;
     }  
}

struct Edge* tail(struct Edge* head) {
    struct Edge* node_ptr = head;
    while (node_ptr->next != NULL) {
        node_ptr = node_ptr->next;
     }   
    return node_ptr;
}

void append(struct Edge* head, FunctionNode* vertex) {
    struct Edge* tail_ptr = tail(head);
    struct Edge* node = create(vertex, -1);
    tail_ptr->next = node;
    node->prev = tail_ptr;
}

void remove(struct Edge* head, int node_id) {
    struct Edge* node_ptr = head;
    while (node_ptr->next != NULL) {
        if(node_ptr->vertex->node_id == node_id) {
            node_ptr->prev->next = node_ptr->next;
            free(node_ptr);
            break;
        }
        node_ptr = node_ptr->next;
    }
}  

#endif