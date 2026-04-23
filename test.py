import sys

# Color Constants
RED = 0
BLACK = 1


class Node:
    def __init__(self, key, color=RED):
        self.key = key
        self.color = color   # Newly inserted nodes are red by default (RBT Property 5)
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        return f"{self.key}({'R' if self.color == RED else 'B'})"


class RedBlackTree:
    def __init__(self):
        # Use NIL sentinel node (black) to simplify boundary cases
        self.NIL = Node(key=None, color=BLACK)
        self.root = self.NIL

    def left_rotate(self, x):
        """Left rotate: Pivot on x, lift up right subtree"""
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, y):
        """Right rotate: Pivot on y, lift up left subtree"""
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def insert(self, key):
        """Insert node and repair Red-Black Tree properties"""
        print(f"\n{'='*50}")
        print(f" inserting {key} ...")
        
        # Step 1: Standard BST insertion
        z = Node(key)
        y = self.NIL
        x = self.root

        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        # 新节点左右子树为NIL，颜色设为红色（默认）
        z.left = self.NIL
        z.right = self.NIL
        z.color = RED  # Red insertion: avoid violating black-height property

        print(" After BST insertion:")
        self.print_tree()

        # Step 2: Fix Red-Black Tree properties (may violate Property 2 or 4)
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        """Repair property violations caused by inserting a red node"""
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:  # 父亲是祖父左孩子
                y = z.parent.parent.right         # 叔叔节点

                # Case 1: Uncle y is red -> recolor + move z up
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent

                else:  # Uncle is black (or NIL)
                    # Case 2: z is right child -> left rotate parent, transition to Case 3
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)

                    # Case 3: z is left child -> right rotate grandparent + recolor
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:  # Symmetric case (parent is right child of grandparent)
                y = z.parent.parent.left

                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)

        # 根节点必须是黑色（性质2）
        self.root.color = BLACK
        print(" After fixup:")
        self.print_tree()

    def inorder(self, node=None):
        """Inorder traversal, returns sorted list of keys"""
        if node is None:
            node = self.root
        result = []
        if node != self.NIL:
            result.extend(self.inorder(node.left))
            result.append(node.key)
            result.extend(self.inorder(node.right))
        return result

    def _check_properties(self):
        """Verify the 5 Red-Black Tree properties"""
        print("\n🔍 Red-Black Tree Property Check:")
        
        # Property 1: Each node is either red or black
        if not self._is_valid_color(self.root): 
            print("❌ Property 1 FAILED: Invalid color")
            return False
        
        # Property 2: Root is black (NIL treated as black)
        if self.root.color == RED:
            print("❌ Property 2 FAILED: Root is red!")
            return False
        print("✅ Property 2 OK: Root is black")

        # Property 3: All leaves (NIL) are black
        def check_nil(node):
            if node != self.NIL:
                if node.left.color == RED or node.right.color == RED:
                    return False
                return check_nil(node.left) and check_nil(node.right)
            return True
        
        if not check_nil(self.root):
            print("❌ Property 3 FAILED: Some leaves are red")
            return False
        print("✅ Property 3 OK: All leaves (NIL) are black")

        # Property 4: Children of red nodes must be black (no double red)
        def no_red_children(node):
            if node == self.NIL:
                return True
            if node.color == RED:
                if node.left.color == RED or node.right.color == RED:
                    print(f"❌ Property 4 FAILED: Red node {node.key} has red child")
                    return False
            return no_red_children(node.left) and no_red_children(node.right)
        
        if not no_red_children(self.root):
            return False
        print("✅ Property 4 OK: No red-red parent-child")

        # Property 5: All paths from root to leaves have the same black height
        def check_black_height(node):
            if node == self.NIL:
                return 1
            left_bh = check_black_height(node.left)
            right_bh = check_black_height(node.right)
            if left_bh != right_bh:
                print(f"❌ Property 5 FAILED: Black heights differ at {node.key}")
                return -1
            return left_bh + (0 if node.color == RED else 1)

        bh = check_black_height(self.root)
        if bh > 0:
            print(f"✅ Property 5 OK: All paths have black height = {bh}")
            return True
        return False

    def _is_valid_color(self, node):
        if node == self.NIL:
            return node.color == BLACK
        if node.color not in (RED, BLACK):
            return False
        return (self._is_valid_color(node.left) and 
                self._is_valid_color(node.right))

    # ========= Tree Visualization =========
    def print_tree(self):
        """ASCII tree visualization output"""
        if self.root == self.NIL:
            print("Empty tree")
            return
        
        lines, *_ = self._print_tree_helper(self.root, 0, False, "")
        for line in lines:
            print(line)

    def _print_tree_helper(self, node, level=0, is_left=False, prefix=""):
        """Recursively generate tree diagram"""
        if node == self.NIL:
            return [], 0, 0, 0

        color_char = "●" if node.color == RED else "■"
        key_str = f"{color_char}{node.key}"
        
        # 右子树
        lines, n, p, x = self._print_tree_helper(node.right, level + 1, False, "")
        
        # 当前节点行
        first_line = (x * ' ') + (n - x - 1) * '_' + key_str + (p - n + 1) * '_'
        second_line = (x * ' ') + '|' + (n + p - x) * ' '
        
        # 左子树
        left_lines, left_n, left_p, left_x = self._print_tree_helper(node.left, level + 1, True, "")
        
        # 合并左右子树
        if left_n > 0:
            second_line = (left_x * ' ') + '/' + (n + p - x - left_x - 1) * ' ' + '|' + (left_n - left_x - 1) * ' '
            first_line = (left_x * ' ') + (left_p - left_n + 1) * '_' + key_str + (n - x - 1) * '_'
        
        # 拼接所有行
        lines = [first_line, second_line] + [a + (n + p - len(a)) * ' ' for a in left_lines + lines]
        return lines, n + left_n + 1, max(p, left_p) + 1, max(left_x + left_n // 2, x + 1)

    def get_black_height(self):
        """Calculate black height (black nodes from root to leaf)"""
        def bh(node):
            if node == self.NIL:
                return 0
            return (0 if node.color == RED else 1) + max(bh(node.left), bh(node.right))
        return bh(self.root)


# ========= Demo Program =========
def demo():
    print("🚀 Red-Black Tree Insertion Demo (Python Implementation)")
    print("Rules: New nodes are red; root must be black; red node's children must be black; all paths from root have same black height.\n")

    rbt = RedBlackTree()
    
    # 测试用例
    keys = [10, 20, 30, 15, 25, 5, 1, 40, 35]
    
    for key in keys:
        rbt.insert(key)
        print("\n✅ Current tree state:")
        rbt.print_tree()
        
        # 验证性质
        if not rbt._check_properties():
            print("❌ Tree is invalid! Stopping.")
            return
        
        # 中序遍历验证BST有序性
        inorder = rbt.inorder()
        assert inorder == sorted(inorder), "BST order violated!"
    
    print("\n" + "="*50)
    print("🎉 All insertions complete! Red-Black Tree built successfully!")
    print(f"Inorder Result: {rbt.inorder()}")
    print(f"Root Node: {rbt.root.key} ({'R' if rbt.root.color == RED else 'B'})")
    print(f"Total Black Height: {rbt.get_black_height()}")


if __name__ == "__main__":
    demo()

