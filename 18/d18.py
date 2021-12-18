from json import loads
from math import floor, ceil

print('Day 18 of Advent of Code!')

raw_data = ''''''

EXPLOSIVE_DEPTH = 4
SPLITTABLE = 10

def _update_depth(root):
    if root:
        _update_depth(root.left)
        root.depth += 1
        _update_depth(root.right)

class Node:
    def __init__(self, data, parent, depth=1):
        
        if data == None:
            self.left = None
            self.right = None
            self.parent = None
            self.val = None
            self.parent = None
            self.depth = depth
        
        elif type(data) is list:
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

    def should_split(self):
        return self.val and self.val >= SPLITTABLE

    def explode(self):
        if self.val is not None:
            raise Exception('Non-leaf cannot explode')
        
        prev, nxt = find_prev(self.left), find_next(self.right)

        if prev:
            prev.val += self.left.val
        if nxt:
            nxt.val += self.right.val

        self.val = 0
        self.left = None
        self.right = None

    def split(self):
        if self.val is None or self.val < SPLITTABLE:
            raise Exception('This node cannot split')
        
        left_val, right_val = floor(self.val/2), ceil(self.val/2)

        self.val = None
        self.left = Node(left_val, self, self.depth + 1)
        self.right = Node(right_val, self, self.depth + 1)

    def add(self, other_data):
        new_root = Node(data=None, parent=None, depth=0)
        other = Node(other_data, new_root)
        self.parent = new_root
        new_root.left = self
        new_root.right = other
        _update_depth(new_root)
        
        # update all nodes depth
        return new_root
    
    def __repr__(self):
        #return f'V:{self.val}/d{self.depth}' if self.val is not None else f'[{self.left},{self.right},d{self.depth}]'
        return f'{self.val}' if self.val is not None else f'[{self.left},{self.right}]'


def find_prev(node: Node)  -> Node:    
    def find_rightmost_leaf(node):
        if node.val is not None:
            return node
        else:
            return find_rightmost_leaf(node.right)

    current_parent = node.parent

    # predecessor on the same level?
    if current_parent.left.val is not None and current_parent.left is not node:
        return current_parent.left
    
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
        return current_parent.right
    
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

def find_splitting_value(node: Node) -> None:
    # in-order traversal until a value to split is found
    current = node
    stack = []
         
    while True:
        if current is not None:
            stack.append(current)
            current = current.left
        elif stack:
            current = stack.pop()
            if current.should_split():
                return current
            current = current.right
        else:
            break
    return None

def add_line_to_tree(tree, line):
    tree = tree.add(line)
    #print(f'{tree}')

    explosive, splittable = find_explosive_pair(tree), find_splitting_value(tree)
    
    while explosive or splittable:
        #print(f'   ---> Now to explode: {explosive}. To split: {splittable}')
        if explosive:
            #print(f'BOOM {explosive}\t', end='\t')
            explosive.explode()
            #print(f'After explode:\t{tree}')
            explosive, splittable = find_explosive_pair(tree), find_splitting_value(tree)
            #print(f'   ---> Now to explode: {explosive}. To split: {splittable}')
            continue        
        elif splittable:
            #print(f'SPLIT {splittable}\t', end='\t')
            splittable.split()
            explosive, splittable = find_explosive_pair(tree), find_splitting_value(tree)
            #print(f'After split:\t{tree}')
            #print(f'   ---> Now to explode: {explosive}. To split: {splittable}')
            continue
    #print(f'LEFT to explode: {explosive}. To split: {splittable}')

    return tree

def calc_magnitude(tree: Node):
    acc = 0
    if tree.left.val != None:
        acc += 3 * tree.left.val
    else:
        acc += 3 * calc_magnitude(tree.left)
    if tree.right.val != None:
        acc += 2 * tree.right.val
    else:
        acc += 2 * calc_magnitude(tree.right)
    return acc


raw_data = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

data = raw_data.splitlines()
tree = Node(loads(data[0]), None)
for line in data[1:]:
    new_line = loads(line)
    tree = add_line_to_tree(tree, new_line)

print(calc_magnitude(tree))


print('Tests...')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    data = raw_data.splitlines()
    tree = Node(loads(data[0]), None)
    for line in data[1:]:
        new_line = loads(line)
        tree = add_line_to_tree(tree, new_line)

    print(calc_magnitude(tree))
