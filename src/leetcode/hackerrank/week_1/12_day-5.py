#  ==== Day5.1 Merge two sorted linked lists ====

class SinglyLinkedList:
    def __init__(self, d, nxt):
        self.data: int = d
        self.next: SinglyLinkedList = nxt

llist3 = SinglyLinkedList(7,None)
llist2 = SinglyLinkedList(3,llist3)
llist1 = SinglyLinkedList(1,llist2)

llist2_2 = SinglyLinkedList(7,None)
llist1_2 = SinglyLinkedList(1,llist2_2)

def mergeLists(head1, head2):
    current = SinglyLinkedList(0,None)
    dummy = current
    while head1 and head2:
        if head1.data < head2.data:
            current.next = head1
            head1 = head1.next
        else:
            current.next = head2
            head2 = head2.next

        current = current.next

    # Attach the remaining nodes
    current.next = head1 if head1 else head2
    return dummy.next


def print_ll(str1, merged_ll):
    print(str1)
    while merged_ll:
        print(merged_ll.data)
        merged_ll = merged_ll.next

print_ll('llist1', llist1)
print_ll('llist1_2',llist1_2)

merged_ll = mergeLists(llist1,llist1_2)

print_ll('ll_merged',merged_ll)



#  ==== Day5.2 Queue using Two Stacks ====
def Queue_using_Two_Stacks():
    queue1 = []
    def enqueue(payload):
        print("enqueue (1) :: payload", payload)
        queue1.append(payload)

    def dequeue():
        print("dequeue")
        return queue1.pop()

    def printqueue():
        for i in queue1:
            print(i)

    queriesDict = {
        'enqueue': enqueue,
        'dequeue': dequeue,
        'printqueue': printqueue
    }

    q: int = int(input('no of queries : '))

    queries = []
    for i in range(q):
        query = list(map(int, input('enter query : ').rstrip().split()))
        queries.append(query)

    print("queries", queries)

    for i in range(q):
        action = queries[i][0]
        print("=== ",action)
        if action == 1:
            payload = queries[i][1]
            queriesDict.get("enqueue")(payload)
        if action == 2:
            queriesDict.get("dequeue")()
        if action == 3:
            queriesDict.get("printqueue")()

# Queue_using_Two_Stacks() # ✅

#  ==== Day5.3 Balanced Brackets ====

def isBalanced(s):
    stack = []
    bracket_map = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in bracket_map.values():
            stack.append(char)
        elif char in bracket_map:
            if not stack or stack[-1] != bracket_map[char]:
                return "NO"
            stack.pop()

    return "YES" if not stack else "NO"


print(isBalanced('[]'))
print(isBalanced('[()]'))
print(isBalanced('[()}'))