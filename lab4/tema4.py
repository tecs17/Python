#1 Write a function that receives as parameters two lists a and b 
# and returns a list of sets containing: (a intersected with b, a reunited with b, a - b, b - a)

def ex1(a,b):
    a_set = set(a)
    b_set = set(b)
    resultList = list()
    resultList.append(a_set.intersection(b_set))
    resultList.append(a_set.union(b_set))
    resultList.append(a_set-b_set)
    resultList.append(b_set-a_set)

    return resultList

a = [1,2,3,4]
b=[3,4,10,11]

result = ex1(a,b)
print("#1: ")
for s in result:
    print(s)

#2 Write a function that receives a string as a parameter and returns a 
# dictionary in which the keys are the characters in the character string
#  and the values are the number of occurrences of that character in the given 
# text. Example: For string "Ana has apples." given as a parameter the function will return the dictionary:

#{'a': 3, 's': 2, '.': 1, 'e': 1, 'h': 1, 'l': 1, 'p': 2, ' ': 2, 'A': 1, 'n': 1} .
def dict_from_string(string):
    resultDict = {}
    for chr in string:
        resultDict[chr] = resultDict.get(chr, 0) + 1
    return resultDict

string = "Ana has apples."
result = dict_from_string(string)
print(f"\n#2: {result}")

#3 Compare two dictionaries without using the operator "==" returning 
# True or False. (Attention, dictionaries must be recursively covered 
# because they can contain other containers, such as dictionaries, lists, sets, etc.)

def compare_dictionaries(dict1, dict2):
    if not (isinstance(dict1, dict) and isinstance(dict2, dict)):
        return False
    
    if dict1.keys() != dict2.keys():
        return False
    
    for key in dict1:
        values1 = dict1[key]
        values2 = dict2[key]
        
        if isinstance(values1, dict) and isinstance(values2, dict):
            if not compare_dictionaries(values1, values2):
                return False
        
        elif isinstance(values1, set) and isinstance(values2, set):
            if values1 != values2:
                return False
        
        elif isinstance(values1, (list, tuple)) and isinstance(values2, (list, tuple)):
            if len(values1) != len(values2):
                return False
            for i in range(len(values1)):
                if isinstance(values1[i], dict) and isinstance(values2[i], dict):
                    if not compare_dictionaries(values1[i], values2[i]):
                        return False
                elif values1[i] != values2[i]:
                    return False
        
        else:
            if values1 != values2:
                return False

    return True

# true
dict1 = {
    "key1": [1, 2, 3],
    "key2": {"nested_key1": {1, 2, 3}, "nested_key2": (4, 5)},
    "key3": (10, 20, 30),
    "key4": 50,
    "key5": {"sub_key": {"sub_nested_key": "hello"}},
}

dict2 = {
    "key1": [1, 2, 3],
    "key2": {"nested_key1": {1, 2, 3}, "nested_key2": (4, 5)},
    "key3": (10, 20, 30),
    "key4": 50,
    "key5": {"sub_key": {"sub_nested_key": "hello"}},
}
#false
# dict1 = {
#     "key1": [1, 2, 3],
#     "key2": {"nested_key1": {1, 2, 3}, "nested_key2": (4, 5)},
#     "key3": (10, 20, 30),
#     "key4": 50,
#     "key5": {"sub_key": {"sub_nested_key": "hello"}},
# }

# dict2 = {
#     "key1": [1, 2,3],  
#     "key2": {"nested_key1": {1, 2,3}, "nested_key2": (4, 5)},  
#     "key3": (10, 20),  
#     "key4": 50,
#     "key5": {"sub_key": {"sub_nested_key": "world"}},  
# }


print(f"\n#3: {compare_dictionaries(dict1, dict2)}")

#4
def build_xml_element(tag,content, **atributes):
    dictionary=dict(atributes)
    element="<"
    element+=tag
    for key in dictionary.keys():
        element+=" "
        element+=key
        element+="=\" "
        element+=dictionary[key]
        element+="\" "
    element+=">"
    element+=content
    element+="</"
    element+=tag
    element+=">"
    return element 

result = build_xml_element("a", "Hello there", href="http://python.org", _class="my-link", id="someid")
print(f"\n#4: {result}")

#5
def validate_dict(rules,dictionary):
    for rule in rules:
        rule_key = rule[0]
        if rule_key not in dictionary:
            continue
        rule_prefix = rule[1]
        rule_middle = rule[2]
        rule_suffix = rule[3]

        string = dictionary.get(rule_key)
        
        if string.startswith(rule_prefix) == False:
            return False
        if string.endswith(rule_suffix) == False:
            return False
        if rule_middle not in string:
            return False
    return True

rules = {
    ("key1", "", "inside", ""), 
    ("key2", "start", "middle", "winter")
}

dictionary = {
    "key1": "O inside, it's too cold out", 
    "key2": "start is middle not winter"
}

result = validate_dict(rules, dictionary)
print(f"\n#5: {result}")

#6
def ex6(i_list):
    a = set()
    b = set()

    for element in i_list:
        if element in a:
            b.add(element)
            continue
        a.add(element)
    
    return (len(a)-len(b),len(b))

list = [1,1,2,3,4,5,5]
print(f"\n#6: {ex6(list)}")


#7
def ex7(*sets):
    list_of_sets = []
    for set in sets:
        list_of_sets.append(set)
    operators = {" | ", " & ", " - ", " -- "}
    dictionary = dict()
    
    for i in range(len(list_of_sets) - 1):
        for j in range(i + 1, len(list_of_sets)):  
            for op in operators:
                key=str(list_of_sets[i])
                key+=op
                key+=str(list_of_sets[j])  
                if op == " | ":
                    dictionary[key] = list_of_sets[i] | list_of_sets[j]
                elif op == " & ":
                    dictionary[key] = list_of_sets[i] & list_of_sets[j]
                elif op == " - ":
                    dictionary[key] = list_of_sets[i] - list_of_sets[j]
                elif op == " -- ":
                    dictionary[key] = list_of_sets[j] - list_of_sets[i]  
    return dictionary



result = ex7({1, 2}, {2, 3}, {4, 5}) 
print("\n#7: ")
for cheie, valoare in result.items():   
    print(f"{cheie} = {valoare}")    

#8
def find_loop_in_dict(dict):
    resultList = []
    resultList.append(dict.get("start"))
    while True:
        next_element = dict.get(resultList[-1])
        if next_element in resultList:
            return resultList
        resultList.append(next_element)

print(f"\n#8: {find_loop_in_dict({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'})}")

#9
def ex9(*args,**kwargs):
    counter = 0
    for arg in args:
        if arg in kwargs.values():
            counter+=1
    return counter

print(f"\n#9: {ex9(1, 2, 3, 4, x=1, y=2, z=3, w=5)}")