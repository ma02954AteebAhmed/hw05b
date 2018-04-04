import random
communicator = None
########## Nodes.
# Nodes to be used in trees.

class TreeNode:
    '''A node in a binary tree.'''
    def __init__(self, n):
        self.data = n
        self.left = self.right = None
        

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def num_children(self):
        '''N.num_children() -> int
        Returns the number of children of N that are not None.
        '''
        return sum([1 for child in [self.left, self.right] if child])

class TreapNode(TreeNode):
    '''A node in a treap.'''
    def __init__(self, data, priority):
        super().__init__(data)  # Parent constructor.
        self.priority = priority
        self.parent = None

    def __str__(self):
        return "({}, {})".format(self.data, self.priority)
        
class AvlNode(TreeNode):
    '''A node in an AVL tree.'''
    def __init__(self, data):
        super().__init__(data)  # Parent constructor.
        self.height = 0
        self.parent = None

    def __str__(self):
        return "({}, {})".format(self.data, self.height)

########## Trees. ##########
# Trees utilizing above nodes. Use helper functions defined outside
# the class to achieve functionality.

class Bst:
    '''A BST. Does not contain duplicates. Nodes are of type TreeNode.'''
    def __init__(self):
        self.root = None
        self.size = 0

    def __str__(self):
        return tree_string(self.root)
    
    def __repr__(self):
        return self.__str__()
        
    def add(self, n):
        self.root, added = bst_add(self.root,n)
        if added:
            self.size += 1
        return added
    
    def find(self, n):
        return bst_find(self.root, n)
    
    def remove(self, n):
        self.root, removed = bst_remove(self.root, n)
        if removed:
            self.size -= 1
        return removed

    def clear(self):
        self.__init__()
        
class Treap(Bst):
    '''A treap. Does not contain duplicates. Nodes are of type TreapNode.'''
    max_priority = 1 << 10
    def __init__(self):
        super().__init__()
        self.priorities = set()
        
    def add(self, n):
        priority = random.randint(0, Treap.max_priority)
        while priority in self.priorities:
            priority = random.randint(0, Treap.max_priority)
        self.root, added = treap_add(self.root, n, priority)
        if added:
            self.size += 1
            self.priorities.add(priority)
        return added

    def remove(self, n):
        self.root, removed = treap_remove(self.root, n)
        if removed:
            self.size -= 1
        return removed

    
########## Tree helper functions. ##########

# Work for any type of node above.
    
def tree_string(node, level = 0):
    '''tree_string(node) -> str
    credit: https://stackoverflow.com/questions/20242479/printing-a-tree-data-structure-in-python
    '''
    if not node:
        return '\n'
    prefix = '   '*level
    str = repr(node) + '\n'
    if node.num_children():
        str += prefix + '|_ ' + tree_string(node.left, level+1)
        str += prefix + '|_ ' + tree_string(node.right, level+1)
    return str
    
def tree_size(node):
    '''tree_size(node) -> int
    Returns a string representation of the subtree rooted at node.
    '''
    
    count  = 1
    visited = []
    stack = node.child
    
    while( len(stack) > 0 ):
        
        if stack[-1] not in visited:
            
            count += 1
            visited.append( stack[-1] )
            stack += stack[-1].child
            
        else:
            stack.pop()
	
    return count

def tree_height(node):
    '''tree_height(node) -> int
    Returns the height of the subtree rooted at node. Returns -1 if
    node is None.
    A node's height is the value of its height attribute, if it
    exists. Otherwise it has to be computed.
    See
    - EAFP at https://docs.python.org/3.4/glossary.html
    - https://stackoverflow.com/questions/610883/how-to-know-if-an-object-has-an-attribute-in-python
    '''
    if node == None:
        return -1
     
    if hasattr(node , 'height'):
        return height

    if isempty(node):
        return -1
    
def isempty(node):
    
    if node.left == None and node.right == None:
        return True
    return False

def inorder(n, lst = []):
    '''inorder(node) -> [node content]
    Returns an inorder traversal of the subtree rooted at node; empty
    list if n is None.
    '''
    
    if n:
        
        inorder(n.left , lst)
        lst.append(str(n.data))
        inorder(n.right , lst)
        
    return lst

def preorder(n, ls = []):
    '''preorder(node) -> [node content]
    Returns an preorder traversal of the subtree rooted at node; empty
    list if n is None.
    '''
    if n:
        ls.append(str(n.data))
        preorder(n.left,ls)
        preorder(n.right,ls)
    return ls

def postorder(n, lst = []):
    '''postorder(node) -> [node content]
    Returns an postorder traversal of the subtree rooted at node;
    empty list if n is None.
    '''
    if n:
        postorder(n.left,lst)
        postorder(n.right,lst)
        lst.append(str(n.data))
    return lst


def update_height(node):
    '''update_height(node) -> None
    Updates the value of node's height attribute using the height of
    its children.
    Assumes that node has a height attribute.
    '''

    if node.left != None and node.right == None:
        return (1 + node.left.height)

    elif node.left == None and node.right != None:
        return (1 + node.right.height)

    elif isempty(node) == False:
        return 1 + max( node.left.height , node.right.height )

    return 0

    
def rotate_left(node):
    '''rotate_left(node) -> node
    Returns the root of the tree obtained by rotating node to the
    left. Updates the height attribute of nodes where necessary and if
    the attribute is present.
    '''
    try:
        temp = node.right.left
    except:
        temp = None
    _temp = node.right

    #swapping parent if exist
    if hasattr(node,"parent"):
        swap = node.parent
        node.parent = _temp
        if _temp != None:
            node.right.parent = swap

        # setting grand parent
        if swap != None:
            if swap.left == node:
                swap.left = _temp
            elif swap.right == node:
                swap.right = _temp
    if (temp):
        temp.parent = node

    node.right.left = node
    node.right = temp
    
    return _temp


def rotate_right(node):
    '''rotate_right(node) -> node
    Returns the root of the tree obtained by rotating node to the
    right. Updates the height attribute of nodes where necessary and if
    the attribute is present.
    '''
    try:
        temp = node.left.right
    except:
        temp = None
        
    _temp = node.left

    #swapping parent if exist
    if hasattr(node,"parent"):
        swap = node.parent
        node.parent = _temp
        if _temp != None:
            node.left.parent = swap
        
        # setting grand parent
        if swap != None:
            if swap.left == node:
                swap.left = _temp
            elif swap.right == node:
                swap.right = _temp
    if (temp):
        temp.parent = node
        
    node.left.right = node    
    node.left = temp
    return _temp


########## BST helper functions. ##########

def bst_find(node, n, Mine = False, avl = False):
    '''bst_find(node, int) -> bool
    Returns whether n is contained in the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.
    '''
    #print(node)
    if node == None:
        return False

    if Mine == True and avl == False:
        try:
            if node.left.data == n:
                return (node, "left", node.left)
        except:
            pass
        
        try:
            if node.right.data == n:
                return (node, "right", node.right)
        except:
            pass
            
    if node.data < n :
        node = node.right
        return bst_find(node,n,Mine, avl)

    elif node.data > n :
        node = node.left
        return bst_find(node,n,Mine, avl)
        

    elif node.data == n:
        if Mine == True:
            return node
        else:
            return True

def bst_find_min(node, Mine = False, pred = False):
    '''bst_find_min(node) -> int
    Returns the smallest value stored in the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.
    '''
    if node == None:
        return None
    
    try:
        if pred == True and node.left.left == None:
            return node
    except:
        pass
    
    if node.left != None:
        node = node.left
        return bst_find_min(node,Mine,pred)

    else:
        if Mine == True:
            return node
        else: 
            return node.data

def bst_find_max(node, pred = False):
    '''bst_find_max(node) -> int
    Returns the largest value stored in the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.
    '''
    if node == None:
        return None
    try:
        if pred == True and node.right.right == None:
            return node
    except:
        pass

    if node.right != None:
        node = node.right
        return bst_find_max(node, pred)
    
    else:
        return node

    
def bst_add(node, n):
    '''bst_add(node, int) -> (node, bool)
    Returns the result of adding n to the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.
    The first returned value is the root of the tree obtained as a
    result of the addition. The second value indicates whether
    addition succeeded. Addition fails if n is already present in the
    subtree.
    '''
    root = node
    if node == None :
        node = TreeNode(n)
        return (node , True)

    if node.left == None and n < node.data:
        node.left = TreeNode(n)

        return (node,True)

    
    if node.right == None and n > node.data:
        node.right = TreeNode(n)
        return (node,True)

    elif ( n > node.data ):
        node = node.right
        x = bst_add(node,n)[1]

    elif ( n < node.data ):
        node = node.left
        x = bst_add(node,n)[1]

    elif ( n == node.data ):
        return (node,False)
    
    return (root , x)
    
def bst_remove(node, n):
    '''bst_remove(node, int) -> (node, bool)
    Returns the result of removing n from the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.
    The first returned value is the root of the tree obtained as a
    result of the removal. The second value indicates whether removal
    succeeded. Removal fails if n is not present in the subtree.
    '''

    target = cmd = pred = None
    root = node
    found = bst_find(root,n,True)
    if type(found) == bool:
        return (root,False)
    if type(found) == tuple:
        pred = found[0]
        cmd = found[1]
        target = found[2]
    else:
        target = found
        
    if type(found) == TreeNode or type(found) == AvlNode or type(found) == TreapNode:
        return root_remover(node , n)
    
    if (target.left == None and target.right == None):
        return remove_helper(root, found)

    if target.left != None and target.right != None:
        
        ''' t_succ is the parent of the node which is the immediate successor of node to be deleted'''
        t_succ = bst_find_min(target.right, True, True)

        try:   
            t_succ.left.data , target.data = target.data , t_succ.left.data
            if t_succ.left.right != None:
                t_succ.left = bst_remove( t_succ.left , t_succ.left.data)[0]
                return (root,True)
            
            t_succ.left = None
            return (root, True)
        
        except:
            if t_succ == target.right:
                target.data , t_succ.data = t_succ.data , target.data
                target.right = bst_remove(target.right,n)[0]
                return (root,True)
            
            t_succ.data , target.data = target.data , t_succ.data
            bst_remove(t_succ,t_succ.data)
            return (root,True)

    elif target.left == None or target.right == None:
        
        if target.left != None:
            return (root , parent_changer(root, cmd, target.left , pred))
        else:
            return (root, parent_changer(root, cmd, target.right , pred))


def parent_changer(root, side , child , n_parent):
    ''' this function is used to tackle the case when the node to be removed has only one child either left or
        right, and only change of parent is required. '''
    
    if hasattr(child,"parent") and n_parent != None:
        child.parent = n_parent

    if side == "left":
        n_parent.left = child
    else:
        n_parent.right = child

    communicator = n_parent

    return True

def remove_helper(root,found):
    if type(found) == tuple:
        
        if found[1] == "right":
            found[0].right = None
            
        else:
            found[0].left = None
            
        return (root, found[2].data)

    elif type(found) == TreeNode:
        root = None
        return (root, found.data)


def root_remover(root,n):
    if root.left != None:
        root = rotate_right( root )
        return bst_remove( root , n )

    elif root.right != None:

        root = rotate_left( root )
        return bst_remove( root,n )

    else:
        return ( None , True )
    

    

########## BST helper functions. ##########

def treap_bst_add(node, n , p):
    
    new = node
    if node == None:
        node = TreapNode(n,p)
        node.parent = None
        return (node , True)

    if node.left == None and n < node.data:
        new = TreapNode(n,p)
        node.left = new
        node.left.parent = node
        return (new,True)

    if node.right == None and n > node.data:
        new = TreapNode(n,p)
        node.right = new
        node.right.parent = node
        return (new,True)

    elif ( n > node.data ):
        node = node.right
        pkg = treap_bst_add(node,n,p)
        new , x = pkg
        

    elif ( n < node.data ):
        node = node.left
        pkg = treap_bst_add(node,n,p)
        new , x = pkg

    elif ( n == node.data ):
        return (node,False)
    
    return (new , x)


def treap_add(node, n, p):
    '''treap_add(node, int, int) -> (node, bool)
    Returns the result of adding n with priority, p, to the subtree
    rooted at node. Assumes the subtree to be a treap with no
    duplicate values.
    The first returned value is the root of the treap obtained as a
    result of the addition. The second value indicates whether
    addition succeeded. Addition fails if n is already present in the
    subtree.
    '''
    added = treap_bst_add(node , n , p)
    if added[1] == False:
        return ( node , False )
    
    ''' now we have foundd the node we added i.e. added[0] i.e new '''

    new = added[0]
    if new.parent == None:
        return ( new , True )

    ''' now we check the heap property, if priority of added node is greater than
        its predecessor we rotate the inserted node to the left , till the property
        is satisfied '''
    
    direction = None

    while(True):
        
        if new.priority < new.parent.priority:

            if new.data > new.parent.data:
                direction = "right"

            elif new.data < new.parent.data:
                direction = "left"

            if direction == "left":
                
                if new.parent == node:
                    new_root = rotate_right(new.parent)
                    print(new_root)
                    return ( new_root , True )
                
                rotate_right(new.parent)
                
            elif direction == "right":
                
                if new.parent == node:
                    new_root = rotate_left(new.parent)
                    #print(new_root)
                    return ( new_root , True )
                
                rotate_left(new.parent)

        else:
            break
    return ( node , True )

    
def treap_remove(node, n):
    '''treap_remove(node, int) -> (node, bool)
    Returns the result of removing n from the subtree rooted at
    node. Assumes the subtree to be a treap with no duplicate values.
    The first returned value is the root of the treap obtained as a
    result of the removal. The second value indicates whether removal
    succeeded. Removal fails if n is not present in the subtree.
    '''
    
    return bst_remove(node,n) 

########## AVL helper functions. ##########
class AvlTree(Bst):
    '''An AVL tree. Does not contain duplicates. Nodes are of type AvlNode.'''
    def __init__(self):
        super().__init__()
        
    def add(self, n):
        self.root, added = avl_add(self.root, n)
        if added:
            self.size += 1
        return added

    def remove(self, n):
        pass
        self.root, removed = avl_remove(self.root, n)
        if removed:
            self.size -= 1
        return removed



    
def avl_balanced(node):
    '''avl_balanced(node) -> bool
    Returns whether the AVL property is satisfied at node. Should work
    for any of the nodes defined above.
    '''
    if node.left == None and node.right != None:
        if ( node.right.height + 1 ) > 1:
            return "right-heavy"

    elif node.left != None and node.right == None:
        if ( node.left.height + 1 ) > 1:
            return "left-heavy"

    
    elif isempty(node) == True:
        return "balanced"

    elif node.left != None and node.right != None:
        
        if (node.right.height+1) - (node.left.height+1) < -1:
            return "left-heavy"

        elif (node.right.height+1) - (node.left.height+1) > 1:
            return "right-heavy"

    return "balanced"    

def avl_left_left(node):
    '''avl_left_left(node) -> node
    
    Returns the root of the tree obtained by resolving a left-left
    case at node.
    '''
    z = node
    y = z.left
    x = y.left
    
    rotate_right(z)

    x.height = update_height(x)
    z.height = update_height(z)
    y.height = update_height(y)
    return y

def avl_right_right(node):
    '''avl_right_right(node) -> node
    
    Returns the root of the tree obtained by resolving a right_right
    case at node.
    '''
    z = node
    y = z.right
    x = y.right
    
    rotate_left(z)

    x.height = update_height(x)
    z.height = update_height(z)
    y.height = update_height(y)
    return y

def avl_left_right(node):
    '''avl_left_right(node) -> node
    
    Returns the root of the tree obtained by resolving a left_right
    case at node.
    '''
    z = node
    y = z.left
    x = y.right
    
    rotate_left(y)
    rotate_right(z)

    z.height = update_height(z)
    y.height = update_height(y)
    x.height = update_height(x)

    return x

def avl_right_left(node):
    '''avl_right_left(node) -> node
    
    Returns the root of the tree obtained by resolving a right_left
    case at node.
    '''
    z = node
    y = z.right
    x = y.left

    rotate_right(y)
    rotate_left(z)

    z.height = update_height(z)
    y.height = update_height(y)
    x.height = update_height(x)    

    return x


def avl_add(node, n):

    # step 1: adding in the bst fashion..
    x = avl_bst_add(node,n)

    if x[1] == False:
        return (node , False)

    if node == None:
        return x
    # now we find the node, that we added
    found = bst_find( node, n, True, True )

    
    # handling the exception, that we are adding 2nd node in the bst..
    if found.parent == node:
        node.height = update_height(node)
        return (node, True)

    # now we search for unbalanced node
    g = unbalance_finder(found)
    unbalanced = g[0]
    weight = g[1]
    
    #now we have found the unbalanced node
    if unbalanced != None :
        if unbalanced.parent != None:
        
            if unbalanced.parent.left ==  unbalanced:
                old_parent = unbalanced.parent
                old_parent.left = re_balance( unbalanced, weight , n )

            else:    
                old_parent = unbalanced.parent
                old_parent.right = re_balance(unbalanced, weight , n)
        else:
            node = re_balance(unbalanced , weight, n)
            
        height_maintain(unbalanced)
        
    else:
        height_maintain(found)
        
    return (node, True)


def unbalance_finder(node):
    ''' finds the node where disbalance has occure due to insertion or deletion in AVL tree '''
    weight = "balanced"
    ptr = node
    
    while(ptr):

        ptr.height = update_height(ptr)
        weight = avl_balanced(ptr)

        if weight == "left-heavy":
            break

        elif weight == "right-heavy":
            break

        ptr = ptr.parent
        
    return ( ptr , weight )


def re_balance(node, weight, val):
    ''' This function checks the possible cases, that arise because of insertion.
        It performs appropriate rotations rooted at node, and returns a new root. '''

    new_root = None
    
    if weight == "left-heavy":
        # left left case
        if val < node.left.data:
            new_root = avl_left_left(node)

        # left right case
        elif val > node.left.data:
            new_root = avl_left_right(node)

    elif weight == "right-heavy":
        # right right case
        if val > node.right.data:
            new_root = avl_right_right(node)

        # right left case
        elif val < node.right.data:
            new_root = avl_right_left(node)

    return new_root

def height_maintain(node):
    if node == None:
        return 0

    node.height = update_height(node)
    height_maintain(node.parent)
    

def avl_remove(node, n):
    '''avl_remove(node, int) -> (node, bool)
    Returns the result of removing n from the subtree rooted at
    node. Assumes the subtree to be a valid AVL tree with no
    duplicates.
    The first returned value is the root of the AVL tree obtained as a
    result of the removal. The second value indicates whether removal
    succeeded. Removal fails if n is not present in the subtree.
    '''
    target = bst_find(node , n , True, True)

    ''' if removing root '''
    if target.parent == None:
        operation = bst_remove(node, n)

        ''' here we update the height of new root, if it exists '''
        if operation[0]:
            operation[0].height = update_height(operation[0])

        return (operation[0] , operation[1])
    
    operation = bst_remove(node,n)
    status = operation[1]

    if status == False:
        return (root, False)

    ''' now we will find the critical node i.e. the first node with dis-balance in height '''
    critical = communicator
    
    while(critical):

        weight = avl_balanced(target.parent)
        critical_parent = critical.parent

        if weight != "balanced":
            
            if critical_parent == None:
                return ( re_balance( critical , weight , n )  , n )

            if critical_parent.left == critical:
                critical_parent.left = re_balance( critical , weight , n )
            else:
                critical_parent.right = re_balance ( critical , weight , n)
            
    
        critical = critical.parent

    return ( node , n )


def change_parent(pkg):
    ''' it changes the parent of left/right child of node to be deleted. '''
    ''' pkg is a 3-tuple, containing , "node" to be deleted, "right" or "left", if node is
        the left child of its parent "parent" of the node to be deleted i.e. (node,left/right,parent)'''

    node = pkg[0]
    direction = pkg[1]
    grandparent = pkg[2]

    if grandparent != None:

        if direction == "left":

            if node.left != None:
                node.left.parent = grandparent.left

            if node.right != None:
                node.right.parent = grandparent.left

        elif direction == "right":

            if node.left != None:
                node.left.parent = grandparent.right

            if node.right != None:
                node.right.parent = grandparent.right


    return 0

            
    
# we need to take care of height of every node..
def avl_bst_add(node, n):
    
    root = node
    if node == None:
        node = AvlNode(n)
        node.parent = None
        return (node , True)

    if node.left == None and n < node.data:
        node.left = AvlNode(n)
        node.left.parent = node
        return (node,True)

    if node.right == None and n > node.data:
        node.right = AvlNode(n)
        node.right.parent = node
        return (node,True)

    elif ( n > node.data ):
        node = node.right
        x = avl_bst_add(node,n)[1]

    elif ( n < node.data ):
        node = node.left
        x = avl_bst_add(node,n)[1]

    elif ( n == node.data ):
        return (node,False)
    
    return (root , x)






lst = random.sample([i for i in range(200000)],100000)
##s = Bst()
####lst = []
######
####for i in range(10):
####    lst.append(random.randint(0,500))
##
##for i in lst:
##    e = s.add(i)
####
##for i in lst:
##    e = s.remove(i)
##






##avl  = AvlTree()
##lst = []
##
##lst = random.sample([i for i in range(200000)],100000)
##for i in lst:
##    avl.add(i)
