#1
class My_Stack:
    def __init__(self):
        self.elements = []
    def push(self,element):
        self.elements.append(element)
    def pop(self):
        if len(self.elements)== 0:
            return None
        return self.elements.pop()
    def peek(self):
        if len(self.elements) == 0:
            return None
        return self.elements[-1]
    

#2
class My_Queue:
    def __init__(self):
        self.elements =[]
    def push(self,element):
        self.elements.append(element)
    def pop(self):
        if len(self.elements) == 0:
            return None
        return self.elements.pop(0)  
    def peek(self):
        if len(self.elements)== 0:
            return None
        return self.elements[0]

#3
class My_Matrix:
    def __init__(self,n,m):
        if n < 2:
            n=2
        if m<2:
            m=2
        self.n = n
        self.m = m
        self.matrix = [[0 for _ in range(m)] for _ in range(n)]

    def get(self,i,j):
        if i>=self.n or j>=self.m:
            return None
        return self.matrix[i][j]
    
    def set(self,i,j,element):
        if i>=self.n or j>=self.m:
            return None
        self.matrix[i][j]=element

    def transpose(self):
        result_matrix = [[0 for _ in range(self.n)] for _ in range(self.m)]
        for i in range(0,self.n):
            for j in range(0,self.m):
                result_matrix[i][j]=self.matrix[j][i]
        self.matrix = result_matrix
        n_copy=self.n
        self.n = self.m
        self.m = n_copy
    def multiply_with(self,input_matrix):
        if self.m != input_matrix.n:
            print("cannot multiply these matrices")
            return None
        result_matrix = [[0 for _ in range(input_matrix.m)] for _ in range(self.n)]
        
        for i in range(0,self.n):
            for j in range(0,input_matrix.m):
                for k in range(0,input_matrix.n):
                    result_matrix[i][j]+=self.matrix[i][k]*input_matrix.matrix[k][j]
        return result_matrix
    
    def iterate_with_lambda(self,function):
        for i in range(0,self.n):
            for j in range(0,self.m):
                self.matrix[i][j] = function(self.matrix[i][j])
 

test_stack = My_Stack()
test_stack.push(10)
test_stack.push(11)
test_stack.push("string")
test_stack.push(12)
test_stack.pop()
print(test_stack.peek())
print(test_stack.elements)

test_queue = My_Queue()
test_queue.push(2)
test_queue.push(3)
test_queue.push("string")
test_queue.push(4)
test_queue.pop()
print(test_queue.peek())
print(test_queue.elements)

matrix = My_Matrix(2,2)
matrix.set(0,0,1)
matrix.set(0,1,2)
matrix.set(1,0,3)
matrix.set(1,1,4)
print(matrix.get(1,1))

print(matrix.matrix)
matrix.transpose()
print(f"transpose: {matrix.matrix}")
matrix.transpose()

print(f"the matrix multiplied with itself:\n{matrix.multiply_with(matrix)}")

matrix.iterate_with_lambda(lambda x:x+1)
print(f"iterated with lambda x:x+1: {matrix.matrix}")


