#include <stdio.h>
#include <stdlib.h>
// base: https://www.techiedelight.com/trie-implementation-insert-search-delete/
#define CHAR_SIZE 26
#define VALID 0
#define INCOMPLETE -1
#define INCORRECT 1
struct Trie
{
    int isLeaf;    // 1 when node is a leaf node
    struct Trie* character[CHAR_SIZE];
};

struct Trie* getNewTrieNode() {
    struct Trie* node = (struct Trie*)malloc(sizeof(struct Trie));
    node->isLeaf = 0;
    for (int i = 0; i < CHAR_SIZE; i++) {
        node->character[i] = 0;
    }
    return node;
}

void insert(struct Trie *head, char* str) {
    struct Trie* curr = head;
    while (*str) {
        if (curr->character[*str - 'a'] == 0) {
            curr->character[*str - 'a'] = getNewTrieNode();
        }
        curr = curr->character[*str - 'a'];
        str++;
    }
    curr->isLeaf = 1;
}

// Iterative function to search a string in Trie. It returns 1
// if the string is found in the Trie, else it returns 0
int search(struct Trie* head, char* str) {
    struct Trie* curr = head;
    while (*str) {
        //printf("%c\n", *str);
        if (*str < 'a') {
          return INCORRECT;
        }
        if (*str > 'z') {
          return INCORRECT;
        }
        curr = curr->character[*str - 'a'];
        if (curr == 0) {
            return INCORRECT;
        }
        if (curr->isLeaf) {
            return VALID;
        }
        str++;
    }
    if (curr->isLeaf) {
        return VALID;
    } else {
        return INCOMPLETE;
    }
}


