#include "mini_bomb.h"

#include <stdio.h>
#include <string.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

typedef struct TreeNode {
    int value;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static int parse_two_ints(const char *input, int *a, int *b)
{
    char tail;
    return input != NULL && sscanf(input, " %d %d %c", a, b, &tail) == 2;
}

static int parse_one_int(const char *input, int *value)
{
    char tail;
    return input != NULL && sscanf(input, " %d %c", value, &tail) == 1;
}

static int parse_six_ints(const char *input, int values[6])
{
    char tail;

    return input != NULL &&
           sscanf(
               input,
               " %d %d %d %d %d %d %c",
               &values[0],
               &values[1],
               &values[2],
               &values[3],
               &values[4],
               &values[5],
               &tail) == 6;
}

static int phase3_expected(int index)
{
    switch (index) {
    case 0:
        return 602;
    case 1:
        return 311;
    case 2:
        return 707;
    case 3:
        return 256;
    case 4:
        return 389;
    case 5:
        return 911;
    case 6:
        return 128;
    case 7:
        return 444;
    default:
        return -1;
    }
}

static int func4(int target, int low, int high)
{
    int mid = low + (high - low) / 2;

    if (mid == target) {
        return 0;
    }
    if (target < mid) {
        return 2 * func4(target, low, mid - 1);
    }
    return 2 * func4(target, mid + 1, high) + 1;
}

static void reset_nodes(Node nodes[6])
{
    static const int values[6] = {817, 233, 901, 477, 692, 105};
    int index;

    for (index = 0; index < 6; ++index) {
        nodes[index].value = values[index];
        nodes[index].next = index < 5 ? &nodes[index + 1] : NULL;
    }
}

static Node *node_at(Node nodes[6], int position)
{
    Node *current = &nodes[0];
    int step;

    for (step = 1; step < position; ++step) {
        current = current->next;
    }
    return current;
}

static int fun7(const TreeNode *node, int target)
{
    if (node == NULL) {
        return -1;
    }
    if (target < node->value) {
        return 2 * fun7(node->left, target);
    }
    if (target == node->value) {
        return 0;
    }
    return 2 * fun7(node->right, target) + 1;
}

int bomb_phase_1(const char *input)
{
    return input != NULL && strcmp(input, "Assembly reveals intent.") == 0;
}

int bomb_phase_2(const char *input)
{
    int values[6];
    int index;

    if (!parse_six_ints(input, values) || values[0] != 1) {
        return 0;
    }
    for (index = 1; index < 6; ++index) {
        if (values[index] != values[index - 1] * 2) {
            return 0;
        }
    }
    return 1;
}

int bomb_phase_3(const char *input)
{
    int index;
    int value;

    if (!parse_two_ints(input, &index, &value)) {
        return 0;
    }
    return phase3_expected(index) == value;
}

int bomb_phase_4(const char *input)
{
    int target;
    int path;

    if (!parse_two_ints(input, &target, &path)) {
        return 0;
    }
    if (target < 0 || target > 14) {
        return 0;
    }
    return func4(target, 0, 14) == 6 && path == 6;
}

int bomb_phase_5(const char *input)
{
    static const char table[] = "tracebulkmdifnso";
    char output[7];
    int index;

    if (input == NULL || strlen(input) != 6) {
        return 0;
    }
    for (index = 0; index < 6; ++index) {
        output[index] = table[((unsigned char)input[index]) & 0x0f];
    }
    output[6] = '\0';
    return strcmp(output, "traces") == 0;
}

int bomb_phase_6(const char *input)
{
    int values[6];
    int seen[7] = {0};
    Node nodes[6];
    Node *ordered[6];
    int index;

    if (!parse_six_ints(input, values)) {
        return 0;
    }

    for (index = 0; index < 6; ++index) {
        if (values[index] < 1 || values[index] > 6 || seen[values[index]]) {
            return 0;
        }
        seen[values[index]] = 1;
        values[index] = 7 - values[index];
    }

    reset_nodes(nodes);
    for (index = 0; index < 6; ++index) {
        ordered[index] = node_at(nodes, values[index]);
    }
    for (index = 0; index < 5; ++index) {
        ordered[index]->next = ordered[index + 1];
    }
    ordered[5]->next = NULL;

    for (index = 0; index < 5; ++index) {
        if (ordered[index]->value < ordered[index + 1]->value) {
            return 0;
        }
    }
    return 1;
}

int bomb_secret_phase(const char *input)
{
    TreeNode n6 = {6, NULL, NULL};
    TreeNode n20 = {20, NULL, NULL};
    TreeNode n35 = {35, NULL, NULL};
    TreeNode n45 = {45, NULL, NULL};
    TreeNode n99 = {99, NULL, NULL};
    TreeNode n1001 = {1001, NULL, NULL};
    TreeNode n22 = {22, &n20, &n35};
    TreeNode n107 = {107, &n99, &n1001};
    TreeNode n8 = {8, &n6, &n22};
    TreeNode n50 = {50, &n45, &n107};
    TreeNode root = {36, &n8, &n50};
    int value;

    if (!parse_one_int(input, &value)) {
        return 0;
    }
    return fun7(&root, value) == 6;
}
