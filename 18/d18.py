print('Day 18 of Advent of Code!')

raw_data = ''''''

EXPLOSIVE_DEPTH = 4

class Node:
    def __init__(self, data, parent, depth=1):
        
        if type(data) is list:
            #print(f"new node: internal from {data}, depth {depth}")
            self.depth = depth
            self.left = Node(data[0], self, depth+1)
            self.right = Node(data[1], self, depth+1)
            self.val = None
            self.parent = parent
        else:
            #print(f"new node: leaf {data}, depth {depth}")
            self.depth = depth
            self.left = None
            self.right = None
            self.val = data
            self.parent = parent

    def is_explosive(self):
        return self.depth > EXPLOSIVE_DEPTH

    def has_only_leafs(self):
        return (self.left and self.left.val != None) and (self.right and self.right.val != None)
    
    def __repr__(self):
        return str(self.val) if self.val is not None else f'[{self.left},{self.right}]'



def find_prev(node: Node)  -> Node:    
    def find_rightmost_leaf(node):
        if node.val is not None:
            return node
        else:
            return find_rightmost_leaf(node.right)

    current_parent = node.parent

    # predecessor on the same level?
    if current_parent.left.val is not None and current_parent.left is not node:
        return current_parent.left.val
    
    else:
        prev_parent = current_parent.parent
        # we tried going left but reached root - no predecessors!
        if current_parent.parent == None:
            return
        # we went up to a 'right' node - looking in its 'left' neighbor
        elif current_parent == prev_parent.right:
            return find_rightmost_leaf(prev_parent.left)
        # we went up, not at root yet, let's go up until we're in a 'right' node
        else:
            return find_prev(current_parent)


def find_next(node: Node) -> Node:
    
    def find_leftmost_leaf(node):
        if node.val is not None:
            return node
        else:
            return find_leftmost_leaf(node.left)
    
    current_parent = node.parent
   
    if current_parent.right.val is not None and current_parent.right is not node:
        return current_parent.right.val
    
    else:
        prev_parent = current_parent.parent

        if current_parent.parent == None:
            return
        
        elif current_parent == prev_parent.left:
            return find_leftmost_leaf(prev_parent.right)
        
        else:
            return find_next(current_parent)

def find_explosive_pair(node: Node) -> Node:
    # in-order traversal until an explosive pair is found
    current = node
    stack = []
         
    while True:
        if current is not None:
            stack.append(current)
            current = current.left
 
        elif stack:
            current = stack.pop()
            if current.is_explosive() and current.has_only_leafs():
                return current
            current = current.right
 
        else:
            break
      
    return None


l = [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
tree = Node(l, None)
print(tree)
print(find_explosive_pair(tree))

#curr = tree.left.left.left
#print(curr)
#print(f'===> Pred = ',find_prev(curr))
#print(f'\n===> Nxt = ',find_next(curr))






print('Tests...')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
