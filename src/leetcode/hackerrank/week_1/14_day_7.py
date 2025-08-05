# https://www.hackerrank.com/challenges/one-week-preparation-kit-tree-preorder-traversal/problem
## pre code 👈🏻
class Node:
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None
        self.level = None

    def __str__(self):
        return str(self.info)

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def create(self, val):
        if self.root == None:
           self.root = Node(val)
        else:
            current = self.root

            while True:
                if val < current.info:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(val)
                        break
                elif val > current.info:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(val)
                        break
                else:
                    break

## My code 👈🏻
def collpase(node):
    result = []

    if node.info is not None:
        result.append(node.info)

    if node.left is not None:
        result += collpase(node.left)

    if node.right is not None:
        result += collpase(node.right)

    return result


def preOrder(root):
    #print(root.__dict__)
    for i in collpase(root):
        print(i,end=" ")


# ==================== week-1 | Day 5 | problem 3 ============

## https://www.hackerrank.com/challenges/one-week-preparation-kit-no-prefix-set/problem
def noPrefix(words):
    n = len(words)
    print_word = None
    for i in range(n):
        if print_word: break
        print(f"\n-- {words[i]} ---")
        for j,w in enumerate(words):
            print(f'comparing {w} in {words[i]} ', ': 🔸skip' if i==j else '')
            if  w in words[i] and i!=j:
                print_word = words[i]
                print(print_word)
                break

    if print_word:
        print('BAD SET')
    else:
        print('GOOD SET')

noPrefix(['aab', 'defgab', 'abcde', 'aabcde', 'bbbbbbbbbb', 'jabjjjad'])


# =============== week-1 | Day 5 | problem 2 ============= ✔️

# https://www.hackerrank.com/challenges/one-week-preparation-kit-tree-huffman-decoding/problem

def decodeHuff(root, s):
    result = ''
    print('encode code', s)

    def traverse(node, i):
        isleaf = node.data and  node.data != '  '
        print(f"isleaf:{isleaf} ( {node.data} ) | s[{i}]: {s[i]}")
        if isleaf:
            nonlocal result
            result += node.data
            print('yes, result: ', result)
        else:
            print(f"No, moving to next | s[{i}]: {s[i]}")
            i+=1
            if s[i] == 0:
                traverse(node.left,i)
            if s[i] == 1:
                traverse(node.right,i)

    traverse(root,0)

    print(result)
    return result
