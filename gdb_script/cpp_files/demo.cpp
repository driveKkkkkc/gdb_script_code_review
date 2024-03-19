# include <iostream>

// 一个二叉树节点类
class TreeNode
{
public:
    TreeNode(int val): val(val), left(nullptr), right(nullptr) {}
    int val;
    TreeNode* left;
    TreeNode* right;
};

// 一个函数，返回一个string类型的值
std::string func()
{
    std::string str = "hello world";
    return str;
}

// 二叉树的前序遍历
void preOrder(TreeNode* root)
{
    if (root == nullptr)
        return;
    std::cout << root->val << std::endl;
    preOrder(root->left);
    preOrder(root->right);
}

// 主函数
int main()
{
    // std::string str = func();
    // std::cout << str << std::endl;
    // return 0;
    // 创建一个二叉树
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    // 左侧子树
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    // 右侧子树
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(7);

    // 前序遍历
    preOrder(root);

    return 0;
}