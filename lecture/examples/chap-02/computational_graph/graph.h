#ifndef GRAPH_H
#define GRAPH_H

struct FunctionNode{
    int (*function_ptr)(int,int);
    int node_id;
    struct Edge* edges;
};

struct FunctionNode* add_node(int (*function_ptr)(int,int), int node_id);
void remove_node(struct FunctionNode*);
void add_edge(struct FunctionNode* u, struct FunctionNode* v);
void remove_edge(struct FunctionNode* u, struct FunctionNode* v);

#endif