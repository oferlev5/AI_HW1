def twoSum(nums, target):
    res = []
    isFound = False
    for i in range(len(nums)):
        for j in range(len(nums)):
            if (i != j) and (nums[i] + nums[j] == target):
                res.append(i)
                res.append(j)
                isFound = True
                break
        if isFound:
            break
    return res


# not possible to solve this problem with complexity less than O(n^2)

def calculate_max_profit(prices):
    max_profit_list = []
    for i in range(len(prices)):
        if i != len(prices) - 1:
            new_prices = prices[i + 1:]
            max_price = max(new_prices)
            max_profit_list.append(max_price - prices[i])
    result = max(max_profit_list)
    if result > 0:
        return result
    else:
        return 0


class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

    def __str__(self):
        return str(self.value)

# Q3.1
def readFile(filePath):
    file = open(filePath, "r")
    file_content = file.read().split(';')
    Node_list = []
    for i in range(len(file_content)):
        node_obj = Node(int(file_content[i]))
        Node_list.append(node_obj)
    for i in range(len(Node_list)):
        if i != len(Node_list) - 1:
            Node_list[i].next = Node_list[i + 1]

    return Node_list[0]


# Q3.2
def getLength(head):
    counter = 1
    while head.next is not None:
        head = head.next
        counter += 1
    return counter



#Q3.3
def sort_in_place(head):
    node = head
    new_list = []
    while node is not None:
        new_list.append(node)
        node = node.next
    n = len(new_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if new_list[j].value > new_list[j + 1].value:
                new_list[j], new_list[j + 1] = new_list[j + 1], new_list[j]

    for i in range(n-1):
        new_list[i].next = new_list[i+1]
    new_list[n-1].next = None
    return new_list[0]


#time complexity is O(n^2)
#space complexity is O(n)



