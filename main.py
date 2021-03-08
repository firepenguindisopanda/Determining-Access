#Definitions of Data object varaibles
class Data:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
    def __str__(self):
        return f'Data(key={self.key}, value={self.value})'

    def __repr__(self):
        return str(self)

#Definitions of TreeNode object variables and methods
class TreeNode:
    def __init__(self, data, parent=None, left=None, right=None):
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        return f'TreeNode({str(self.data)})'

    def __repr__(self):
        return (str(self))

    def num_descendants(self):
        count = 0
        if self.left is None:
            count += 1
            self.left.num_descendants()

        if self.right is None:
            count += 1
            self.right.num_descendants()

        return count


#Beginning of functions that can be used globaly   
def insert_helper(root, key, value):
    if key < root.data.key:
        if root.left is None:
            data = Data(key,value)
            root.left = TreeNode(data, root)
        else:
            insert_helper(root.left, key, value)
    elif key > root.data.key:
        if root.right is None:
            data = Data(key, value)
            root.right = TreeNode(data, root)
        else:
            insert_helper(root.right, key, value)
    else:
        return

def search_helper(root, key):
    if root is None:
        return None
    if root.data.key == key:
        return root
    if key < root.data.key:
        return search_helper(root.left, key)
    return search_helper(root.right, key)

def range_query_helper(root, lo, hi):
    if root is None:
        return []
    res = []
    if root.data.key >= lo and root.data.key <= hi:
        res.append(root)
    res_from_left = range_query_helper(root.left, lo, hi)
    res_from_right = range_query_helper(root.right, lo, hi)
    res = res_from_left + res + res_from_right
    return res

def range_query(root, lo, hi):
    if root is None:
        return []
    if root.data.key >= lo and root.data.key <= hi:
        return range_query_helper(root, lo, hi)
    if root.data.key < lo:
        return range_query(root.right, lo, hi)
    return range_query(root.left, lo , hi)

def lte_query(root, key):
    if root is None:
        return None

    if root.data.key < key:
        others = lte_query(root.right, key)
        if others is None:
            return root
        else:
            return others
    return lte_query(root.left, key)

def gte_query(root, key):
    if root is None:
        return None

    if root.data.key == key:
        return root

    if root.data.key > key:
        others = gte_query(root.left, key)
        if others is None:
            return root
        else:
            return others
    return gte_query(root.right, key)

def to_array(root, arr, index):
    if root is not None:
        arr[index] = root.data.key
        to_array(root.left, arr, index * 2)
        to_array(root.right, arr, index * 2 + 1)

def get_height(root):
    if root is None:
        return 0
    return 1 + max(get_height(root.left), get_height(root.right))
#End of globabl functions definitions
    
    
#Definitions of a BinarySearhTree object variables and methods
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def __bool__(self):
        return not self.is_empty()

    def num_nodes(self):
        if self.root is None:
            return 0
        return self.root.num_descendants()

    def __len__(self):
        return self.num_nodes()

    def insert(self, key, value=None):
        if self.root is None:
            data = Data(key, value)
            self.root = TreeNode(data)
        else:
            insert_helper(self.root, key, value)

    def search(self, key):
        return search_helper(self.root, key)

    def __contains__(self, key):
        return self.search(key) is not None

    def __getitem__(self, key):
        node = self.search(key)
        if node is None:
            self.insert(key, value)
        else:
            node.data.value = value

    def range_query(self, hi, lo):
        return range_query(self.root, hi, lo)

    def lte_query(self, key):
        return lte_query(self.root, key)
    
    def gte_query(self, key):
        return gte_query(self.root, key)


    def get_height(self):
        return get_height(self.root) - 1

    def to_array(self):
        height = self.get_height()
        max_nodes = 2 ** (height + 1) - 1
        arr = [None] * (max_nodes + 1)
        to_array(self.root, arr, 1)
        return arr




log_file = open("log.txt", "r")
query_file = open("queries.txt", "r")
solutions_file = open("solution.txt", "w+")
bst_test = BinarySearchTree()
Invalid_Entry_Dictionary = dict()

count_timestamp_characters =0
count_ip_characters = 0



for log_line in log_file:
    timestamp, ip_address = log_line.split()
    for i in timestamp:
        count_timestamp_characters += 1

    for j in ip_address:
        count_ip_characters += 1

    

    if count_timestamp_characters <= 10 and count_ip_characters <= 15:
        timestamp = int(timestamp)
        bst_data = Data(timestamp, ip_address)
        bst_test.insert(bst_data.key, bst_data.value)
    else:
        if count_timestamp_characters > 10:
            Invalid_Entry_Dictionary.update(timestamp = ip_address)
            print(timestamp, "Isn't a valid entry")
        else:
            Invalid_Entry_Dictionary.update(timestamp = ip_address)
            print(ip_address, "Isn't a valid entry")
        
    count_timestamp_characters = 0
    count_ip_characters = 0





for query_line in query_file:
    first_word = query_line.split(None, 1)[0]
    first_word = str(first_word)
    if first_word == "LTE":
        second_word = query_line.split(None, 2)[1]
        second_word_to_int = int(second_word)
        answer = bst_test.lte_query(second_word_to_int)
        if answer == None:
            solutions_file.write(None)
            solutions_file.write('\n')
        else:
            solutions_file.write(answer.data.value)
            solutions_file.write('\n')
        


    if first_word == "GTE":
        second_word = query_line.split(None,2)[1]
        second_word_to_int = int(second_word)
        answer = bst_test.gte_query(second_word_to_int)
        if answer == None:
            solutions_file.write(None)
            solutions_file.write('\n')
        else:
            solutions_file.write(answer.data.value)
            solutions_file.write('\n')

    
    if first_word == "BTW":
        
        second_word = query_line.split(None, 2)[1]
        second_word_to_int = int(second_word)
        third_word = query_line.split(None, 3)[2]
        third_word_to_int = int(third_word)
        
        if second_word_to_int  < third_word_to_int:
            answer = bst_test.range_query(second_word_to_int, third_word_to_int)
            if answer == []:
                solutions_file.write(None)
                solutions_file.write('\n')
            else:
                answer_length = len(answer)
                for ans in range(answer_length):
                    solutions_file.write(answer[ans].data.value)
                    solutions_file.write(' ')
            
            
        else:
            answer = bst_test.range_query(third_word_to_int, second_word_to_int)
            if answer == []:
                solutions_file.write(None)
                solutions_file.write('\n')
            else:
                answer_length = len(answer)
                for ans in range(answer_length):
                    solutions_file.write(answer[ans].data.value)
                    solutions_file.write('  ')
            
            
        solutions_file.write('\n')
log_file.close()
query_file.close()
solutions_file.close()
