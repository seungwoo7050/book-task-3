#include "mini_bomb.hpp"

#include <array>
#include <sstream>
#include <string>

namespace bomblab {
namespace {

struct Node {
    int value;
    Node *next;
};

struct TreeNode {
    int value;
    TreeNode *left;
    TreeNode *right;
};

template <typename... Ints>
bool parse_exact_ints(std::string_view input, Ints &...values)
{
    std::istringstream stream{std::string(input)};
    char tail = '\0';

    if (!((stream >> values) && ...)) {
        return false;
    }
    return !(stream >> tail);
}

int phase3_expected(int index)
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

int func4(int target, int low, int high)
{
    const int mid = low + (high - low) / 2;

    if (mid == target) {
        return 0;
    }
    if (target < mid) {
        return 2 * func4(target, low, mid - 1);
    }
    return 2 * func4(target, mid + 1, high) + 1;
}

void reset_nodes(std::array<Node, 6> &nodes)
{
    static constexpr std::array<int, 6> values = {817, 233, 901, 477, 692, 105};

    for (std::size_t index = 0; index < nodes.size(); ++index) {
        nodes[index].value = values[index];
        nodes[index].next = index + 1 < nodes.size() ? &nodes[index + 1] : nullptr;
    }
}

Node *node_at(std::array<Node, 6> &nodes, int position)
{
    Node *current = &nodes[0];

    for (int step = 1; step < position; ++step) {
        current = current->next;
    }
    return current;
}

int fun7(const TreeNode *node, int target)
{
    if (node == nullptr) {
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

}  // 내부 helper 이름공간 끝

bool phase1(std::string_view input)
{
    return input == "Assembly reveals intent.";
}

bool phase2(std::string_view input)
{
    std::array<int, 6> values{};

    if (!parse_exact_ints(input, values[0], values[1], values[2], values[3], values[4], values[5])) {
        return false;
    }
    if (values[0] != 1) {
        return false;
    }
    for (std::size_t index = 1; index < values.size(); ++index) {
        if (values[index] != values[index - 1] * 2) {
            return false;
        }
    }
    return true;
}

bool phase3(std::string_view input)
{
    int index = 0;
    int value = 0;

    if (!parse_exact_ints(input, index, value)) {
        return false;
    }
    return phase3_expected(index) == value;
}

bool phase4(std::string_view input)
{
    int target = 0;
    int path = 0;

    if (!parse_exact_ints(input, target, path)) {
        return false;
    }
    if (target < 0 || target > 14) {
        return false;
    }
    return func4(target, 0, 14) == 6 && path == 6;
}

bool phase5(std::string_view input)
{
    static constexpr std::string_view table = "tracebulkmdifnso";
    std::string output;

    if (input.size() != 6) {
        return false;
    }
    output.reserve(input.size());
    for (unsigned char ch : input) {
        output.push_back(table[ch & 0x0f]);
    }
    return output == "traces";
}

bool phase6(std::string_view input)
{
    std::array<int, 6> values{};
    std::array<bool, 7> seen{};
    std::array<Node, 6> nodes{};
    std::array<Node *, 6> ordered{};

    if (!parse_exact_ints(input, values[0], values[1], values[2], values[3], values[4], values[5])) {
        return false;
    }

    for (int &value : values) {
        if (value < 1 || value > 6 || seen[value]) {
            return false;
        }
        seen[value] = true;
        value = 7 - value;
    }

    reset_nodes(nodes);
    for (std::size_t index = 0; index < values.size(); ++index) {
        ordered[index] = node_at(nodes, values[index]);
    }
    for (std::size_t index = 0; index + 1 < ordered.size(); ++index) {
        ordered[index]->next = ordered[index + 1];
    }
    ordered.back()->next = nullptr;

    for (std::size_t index = 0; index + 1 < ordered.size(); ++index) {
        if (ordered[index]->value < ordered[index + 1]->value) {
            return false;
        }
    }
    return true;
}

bool secret_phase(std::string_view input)
{
    int value = 0;
    TreeNode n6{6, nullptr, nullptr};
    TreeNode n20{20, nullptr, nullptr};
    TreeNode n35{35, nullptr, nullptr};
    TreeNode n45{45, nullptr, nullptr};
    TreeNode n99{99, nullptr, nullptr};
    TreeNode n1001{1001, nullptr, nullptr};
    TreeNode n22{22, &n20, &n35};
    TreeNode n107{107, &n99, &n1001};
    TreeNode n8{8, &n6, &n22};
    TreeNode n50{50, &n45, &n107};
    TreeNode root{36, &n8, &n50};

    if (!parse_exact_ints(input, value)) {
        return false;
    }
    return fun7(&root, value) == 6;
}

}  // bomblab 이름공간 끝
