#include <stdlib.h> 
#include <stdbool.h> 

struct Node** create_lists(int n);
void remove_lists(struct Node** adj, int n);
void remove_list(struct Node* head);
void append_node(struct Node* tail, int vertex);
void remove_node(struct Node* head, int vertex);
bool edge_exist(struct Node** adj, int u, int v);
struct Node* tail(struct Node* head);
void clear(struct Node* head);

void add_edge(struct Node** adj, int u, int v);
void remove_edge(struct Node** adj, int u, int v);

struct Node{
    int vertex;
    struct Node* prev;
    struct Node* next;
};

struct Node** create_lists(int n) {
    struct Node** adj = (struct Node**) malloc(n * sizeof(struct Node*));

    for(int i = 0; i < n; i++) {
        adj[i] = (struct Node*) malloc(sizeof(struct Node));
    }

    return adj;
}

void remove_lists(struct Node** adj, int n) {
    for(int i = 0; i < n; i++) {
        struct Node* head = adj[i];
        clear(head);
        free(head);
    }  
    free(adj);
}

void clear(struct Node *head) {
    struct Node* node_ptr = head->next;
    struct Node* tmp; 

    while (node_ptr != NULL) {
        tmp = node_ptr->next;
        free(node_ptr);
        node_ptr = tmp;
     }  
}

struct Node* create_node(int vertex) {
    struct Node* node = (struct Node*) malloc(sizeof(struct Node));
    node->vertex = vertex;
    node->next = NULL;
    return node;
}

void append_node(struct Node* head, int vertex) {
    struct Node* tail_ptr = tail(head);
    struct Node* node = create_node(vertex);
    tail_ptr->next = node;
    node->prev = tail_ptr;
}

void remove_node(struct Node* head, int vertex) {
    struct Node* node_ptr = head->next;
    while (node_ptr != NULL) {
        if(node_ptr->vertex == vertex) {
            node_ptr->prev->next = node_ptr->next;
            free(node_ptr);
            break;
        }
        node_ptr = node_ptr->next;
    }
}  

struct Node* tail(struct Node* head) {
    struct Node* node_ptr = head;
    while (node_ptr->next != NULL) {
        node_ptr = node_ptr->next;
     }   
    return node_ptr;
}

bool edge_exist(struct Node** adj, int u, int v) {
    struct Node* head = adj[u];
    struct Node* node_ptr = head->next;
    bool status = false;
    
    while (node_ptr != NULL) {
        if(node_ptr->vertex == v){
            status = true;
            break;
        }
       node_ptr = node_ptr->next;
    }
    return status;
}

void add_edge(struct Node** adj, int u, int v){
    struct Node* head;
    if(!edge_exist(adj, u, v)) {
        head = adj[u];
        append_node(head, v);
    } 
}

void remove_edge(struct Node** adj, int u, int v){
    struct Node* head;
    if(edge_exist(adj, u, v)) {
        head = adj[u];
        remove_node(head, v);
    }
}