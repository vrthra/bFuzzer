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
        printf("%d\n", *str);
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
        str++;
    }
    if (curr->isLeaf) {
        return VALID;
    } else {
        return INCOMPLETE;
    }
}

int main_tri(char* str) {
    struct Trie* head = getNewTrieNode();
    int r = 0;

    insert(head, "true");
    //r = search(head, "true");
    //printf("true:true %d\n", r);       // print 0
    //r = search(head, "t");
    //printf("true:t %d\n", r);       // print -1 // incomplete
    //r = search(head, "tr");
    //printf("true:tr %d\n", r);       // print -1 // incomplete
    //r = search(head, "trX");
    //printf("true;trX %d\n", r);       // print 1 // incorrect

    insert(head, "false");
    //r = search(head, "false");
    //printf("false:false %d\n", r);  // print 0

    insert(head, "null");
    //r = search(head, "null");
    //printf("null:null %d\n", r);        // print 0

    r = search(head, str);
    return r;
}

FILE* v = 0;
char* read_input() {
    int counter = 0;
    char* chars = malloc(sizeof(char) * 1000);
    int c = 0;
    int eof = EOF;
    while((c = fgetc(v)) != eof){
        if (counter == 1000) {
            exit(-1);
        }
        chars[counter++] = c;
    }
    chars[counter] = '\0';
    return chars;
}

int main(int argc, char** argv) {
    if (argc > 1) {
      v = fopen(argv[1], "r");
    } else {
      v = stdin;
    }
    char* string = read_input();
    if (argc > 1) {
      fclose(v);
    }
    return main_tri(string);
}
