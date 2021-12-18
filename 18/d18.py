print('Day 18 of Advent of Code!')

raw_data = ''''''


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

    def __repr__(self):
        return str(self.val) if self.val is not None else f'[{self.left},{self.right}]'

def find_rightmost_leaf(node):
    print(f'Node: {node}. Node.left {node.left} Node.right {node.right} Node.val {node.val}')
    if node.val is not None:
        print(f"found pred! {node}")
        return node
    else:
        return find_rightmost_leaf(node.right)


def find_prev(node):    
    current_parent = node.parent

    print(f'I am {node}. My parent is {current_parent}')

    if current_parent == None:
        print(f'Reached root from right side, looking in {node.left}')
        return find_rightmost_leaf(node.left)
    
    elif current_parent.left.val is not None and current_parent.left is not node:
        print(f'My predecessor is on the same level')
        return current_parent.left.val
    
    else:
        prev_parent = current_parent.parent

        if current_parent.parent == None:
            print(f'Reached root, no predecessors!')
            return
        
        elif current_parent == prev_parent.right:
            print(f'Found proper node, looking in {prev_parent.left}')
            return find_rightmost_leaf(prev_parent.left)
        
        else:
            print(f'Recursing from {current_parent}')
            find_prev(current_parent)


def find_next(node):
    
    def find_leftmost_leaf(node):
        if node.val is not None:
            return node
        else:
            return find_leftmost_leaf(node.left)
    
    current_parent = node.parent

    print(f'I am {node}. My parent is {current_parent}')
   
    if current_parent.right.val is not None and current_parent.right is not node:
        print(f'My successor is on the same level')
        return current_parent.right.val
    
    else:
        prev_parent = current_parent.parent

        if current_parent.parent == None:
            print(f'Reached root, no successors!')
            return
        
        elif current_parent == prev_parent.left:
            print(f'Found proper node, looking in {prev_parent.right}')
            return find_leftmost_leaf(prev_parent.right)
        
        else:
            print(f'Recursing from {current_parent}')
            find_next(current_parent)



l = [[[[1,1],[2,2]],[3,3]],[4,4]]
l = [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
tree = Node(l, None)
print(tree)

#curr = tree.left.right.right.right
#curr = tree.right.left
curr = tree.right.left.left.left

print(curr)
print(f'Pred',find_prev(curr))
print(f'Nxt',find_next(curr))






print('Tests...')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
