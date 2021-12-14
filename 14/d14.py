import re
from collections import defaultdict

print('Day 14 of Advent of Code!')

raw_data = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''

class Element:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return str(self.val)

class Polymer:
    def __init__(self, data):
        elements = list(data)
        self.head = Element(elements[0])
        current = self.head
        for element in elements[1:]:
            new_element = Element(element)
            current.next = new_element
            current = new_element
    
    def __repr__(self):
        current = self.head
        elements = []
        while current is not None:
            elements.append(current.val)
            current = current.next
        return "".join(elements)

    def insert_between(self, instructions):
        first = self.head
        second = self.head.next
        while second:
            pair = first.val + second.val
            value_to_insert = instructions.get(pair)
            if value_to_insert:
                new_element = Element(value_to_insert)
            first.next = new_element
            first = second
            new_element.next = second
            second = second.next
        
    def count_elements(self):
        current = self.head
        element_counter = defaultdict(int)
        while current is not None:
            element_counter[current.val] += 1
            current = current.next
        return element_counter

def parse_data(data):
    initial, raw_insertions = data.split('\n\n')
    insertions = dict()
    regex = r'(\w+) -> (\w+)'
    for insertion in raw_insertions.splitlines():
        parsed = re.findall(regex, insertion)[0]
        insertions[parsed[0]] = parsed[1]
    polymer = Polymer(initial)
    return polymer, insertions

poly, inserts = parse_data(raw_data)
for _ in range(5):
    poly.insert_between(inserts)
    print(poly)
    print()
counter = sorted(list(poly.count_elements().values()))
print(counter[-1] - counter[0])

print('Tests...')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    #poly, inserts = parse_data(raw_data)
    
