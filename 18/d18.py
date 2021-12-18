from collections import deque

print('Day 18 of Advent of Code!')

raw_data = ''''''


#l = [[[[[9,8],1],2],3],4]
#l = [[[[6,3],[2,6]],[[6,9],[8,1]]],[[[2,1],[7,5]],[[7,3],[7,3]]]]

class Node:
    def __init__(self, data, parent, depth=1):
        
        if type(data) is list:
            print(f"new node: internal from {data}, depth {depth}")
            self.depth = depth
            self.left = Node(data[0], self, depth+1)
            self.right = Node(data[1], self, depth+1)
            self.val = None
            self.parent = parent
        else:
            print(f"new node: leaf {data}, depth {depth}")
            self.depth = depth
            self.left = None
            self.right = None
            self.val = data
            self.parent = parent

    def __repr__(self):
        return str(self.val) if self.val is not None else f'[{self.left},{self.right}]'
    
    
def find_predecessor_leaf(node):
    def find_rightmost_leaf(node):
        if node.val is not None:
            return node
        else:
            return find_rightmost_leaf(node.right)
    
    current_parent = node.parent

    print(f'I am {node}. My parent is {current_parent}')

    if current_parent == None:
        print(f'Reached root from right side, looking in {node.left}')
        return find_rightmost_leaf(node.left)
    
    elif current_parent.left.val is not None and current_parent.left is not node:
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
            find_predecessor_leaf(current_parent)



tree = Node(l, None)
print(tree)

#curr = tree.left.left.left.right
#curr = tree.right.right.right.right.left
#print(curr)
#print(f'Pred',find_predecessor_leaf(curr))




print('Tests...')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
