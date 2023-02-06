class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    def __str__(self):
        return str(self.value)

def putta(node: TreeNode, newvalue):
    if node == None:
        return TreeNode(newvalue)
    if newvalue < node.value:
        node.left = putta(node.left, newvalue)
    if newvalue > node.value:
        node.right = putta(node.right, newvalue)
    return node

def finns(node: TreeNode, value):
    if node == None:
        return False
    if value == node.value:
        return True
    if value < node.value:
        return finns(node.left, value)
    else:
        return finns(node.right, value)

def skriv(node: TreeNode):
    if node == None:
        return
    skriv(node.left)
    print(node.value, end=" ")
    skriv(node.right)

class Bintree:
    def __init__(self):
        self.root = None

    def put(self,newvalue):
        # Sorterar in newvalue i trädet
        self.root = putta(self.root, newvalue)

    def __contains__(self,value):
        # True om value finns i trädet, False annars
        return finns(self.root,value)

    def write(self):
        # Skriver ut trädet i inorder
        skriv(self.root)
        print("\n")