#1 Create a class hierarchy for shapes, starting with a base class Shape. Then, create subclasses like Circle, Rectangle, and Triangle. Implement methods to calculate area and perimeter for each shape.
class Shape:
    def PrintName(self):
        print("I am a shape.")
    def CalculateArea(self):
        pass
    def CalculatePerimeter(self):
        pass

class Circle(Shape):
    def __init__(self,radius):
        self.radius=radius
    def PrintName(self):
        print("I am a circle.")
    def CalculateArea(self):
        return 3.14 * (self.radius**2)
    def CalculatePerimeter(self):
        return 2 * 3.14 * self.radius

class Rectangle(Shape):
    def __init__(self,lungime,latime):
        self.lungime = lungime
        self.latime = latime
    def PrintName(self):
        print("I am a Rectangle")
    def CalculateArea(self):
        return self.lungime * self.latime
    def CalculatePerimeter(self):
        return 2*(self.lungime + self.latime)

class Triangle(Shape):
    def __init__(self,side1,side2,side3):
        self.sides = []
        self.sides.append(side1)
        self.sides.append(side2)
        self.sides.append(side3)
    def PrintName(self):
        print("I am a Triangle")
    def CalculatePerimeter(self):
        return self.sides[0] + self.sides[1] + self.sides[2]
    def CalculateArea(self):
        s = self.CalculatePerimeter() /2
        return (s * (s - self.sides[0]) * (s - self.sides[1]) * ( s - self.sides[2])) ** 0.5 
    
sh = Shape()
triangle = Triangle(2,3,4)
circle = Circle(2)
rectangle =  Rectangle(2,3)

print(f"#1\nTriangle: P={triangle.CalculatePerimeter()}; A={str.format("{0:.3f}",triangle.CalculateArea())}")
print(f"Circle: P={circle.CalculatePerimeter()}; A={circle.CalculateArea()}")
print(f"Rectangle: P={rectangle.CalculatePerimeter()}; A={rectangle.CalculateArea()}")

#2 Design a bank account system with a base class Account and subclasses SavingsAccount and CheckingAccount. Implement methods for deposit, withdrawal, and interest calculation.
class Account:
    def __init__(self,name,balance=0):
        self.name = name
        self.balance=balance
    def deposit(self,amount):
        if amount>0:
            self.balance+=amount  
            return
        print("The amount given must be positive.")
    def withdraw(self,amount):
        if(amount<=0):
            print("The amount must be positive")   
        else:          
            if(self.balance>= amount):
                self.balance-=amount
            else:
                print(f"You only have {self.balance} $ in your account.") 

class SavingsAccount(Account):
    def __init__(self,balance=0,interest_rate=0.05):
        super().__init__(balance)
        self.interest_rate = interest_rate
    def calculate_interest_rate(self):
        return self.interest_rate*self.balance
    def apply_interest(self):
       self.balance+=self.calculate_interest_rate()

class CheckingAccount(Account):
    def __init__(self, name, balance=0, limit=500):
      super().__init__(name, balance)
      self.limit=limit
    def withdraw(self,sum_of_money):
        if (sum_of_money <= 0):
            print("The amount must be positive") 
            return
        if(sum_of_money>self.limit):
            print("You can't exceed the limit.")
            return
        if(sum_of_money > self.balance):
            print(f"You only have {self.balance} $ in your account.")
            return
        self.balance-=sum_of_money

bob = CheckingAccount("Bob",500,limit=100)
ema = SavingsAccount("Ema")
print("\n#2")
bob.deposit(100)
bob.withdraw(50)
bob.withdraw(150)
print(f"bob`s balance:{bob.balance}")

ema.deposit(200)
ema.withdraw(300)
ema.withdraw(100)
ema.apply_interest()
print(f"ema`s balance: {ema.balance}")

#3 Create a base class Vehicle with attributes like maker, model, and year, and then create subclasses for specific types of vehicles like Car, Motorcycle, and Truck. Add methods to calculate mileage or towing capacity based on the vehicle type.
print("\n#3")
class Vehicle:
    def __init__(self,maker,model,year,km,fuel_cap,fuel_consumption):
        self.maker = maker
        self.model = model
        self.year = year
        self.fuel_consumption = fuel_consumption
        self.km=km
        self.fuel_cap=fuel_cap
    def __str__(self):
        return f"({self.maker}, {self.model},{self.year})"
    def calculate_mileage(self,fuel_remaining,):
        return fuel_remaining/self.fuel_consumption

class Car(Vehicle):
    def __init__(self,maker,model,year, km, fuel_cap,fuel_consumption):
        super().__init__(maker,model,year,km,fuel_cap,fuel_consumption)

class Motorcycle(Vehicle):
    def __init__(self,maker,model,year, km, fuel_cap,fuel_consumption):
        super().__init__(maker,model,year,km,fuel_cap,fuel_consumption)

class Truck(Vehicle):
    def __init__(self,maker,model,year, km, fuel_cap,fuel_consumption,full_capacity):
        super().__init__(maker,model,year,km,fuel_cap,fuel_consumption)
        self.full_capacity=full_capacity
    def calculate_towing_capacity(self,load_weight):
        if(self.full_capacity>load_weight):
            self.full_capacity-=load_weight
            return self.full_capacity
        else:
            print("The load is too heavy.")

car = Car("bmw","1","2023",2000,10,4)
motorcycle = Motorcycle("yamaha","2","2021",1000,6,3)
truck = Truck("ford","3",2000,15000,20,5,200)
print(f"{car} mileagle: {car.calculate_mileage(8)}")
print(f"{motorcycle} mileagle: {motorcycle.calculate_mileage(4)}")
print(f"{truck} mileagle: {truck.calculate_mileage(10)}")
truck.calculate_towing_capacity(1000)
truck.calculate_towing_capacity(10)

#4 Build an employee hierarchy with a base class Employee. Create subclasses for different types of employees like Manager, Engineer, and Salesperson. Each subclass should have attributes like salary and methods related to their roles.
print("\n#4")
class Employee:
    def __init__(self,name,salary,holiday_days_remaining,hours_worked):
        self.name = name
        self.salary = salary
        self.holiday_days_remaining = holiday_days_remaining
        self.hours_worked = hours_worked
        self.overtime_hours = 0
        self.available = True
        
class Salesperson(Employee):
    def __init__(self,name,manager,holiday_days_remaining=5,hours_worked=0,salary=1700):
        super().__init__(name,salary,holiday_days_remaining,hours_worked)
        self.manager = manager
        manager.add_member(self)

    def request_vacation(self,days):
        print (self.manager.verify_vacation(self,days)) 

    def work_report(self,hours,sales,money_made):
        self.available = True
        self.hours_worked += hours
        if hours > 8: 
            self.overtime_hours+= hours - 8
        self.manager.receive_sales_report(self,sales,money_made)

class Engineer(Employee):
    def __init__(self,name,manager,holiday_days_remaining=5,hours_worked=0,salary=3400):
        super().__init__(name,salary,holiday_days_remaining,hours_worked)
        self.manager = manager
        manager.add_member(self)

    def request_vacation(self,days):
        print (self.manager.verify_vacation(self,days)) 

    def work_report(self,hours,description):
        self.available = True
        self.hours_worked += hours
        if hours > 8: 
            self.overtime_hours+= hours - 8
        self.manager.receive_progress_report(self,description)
    
class Manager(Employee):
    def __init__(self,name,holiday_days_remaining=5,hours_worked=0,salary=5100):
        super().__init__(name,salary,holiday_days_remaining,hours_worked)
        self.sales = []
        self.progress = []
        self.sales_team=[]
        self.engineering_team=[]
    def add_member(self,employee):
        if isinstance(employee,Salesperson):
            self.sales_team.append(employee)
        else:
            self.engineering_team.append(employee)
    def receive_sales_report(self,employee,sales,money_made):
        self.sales.append((employee.name ,sales,money_made))

    def receive_progress_report(self,employee,description):
        self.progress.append((employee.name,description))

    def verify_vacation(self,employee,days):
        counter = 0
        if isinstance(employee,Employee) == False:
            return "not an employee"
        team = self.engineering_team
        if isinstance(employee,Salesperson):
            team=self.sales_team
        for person in team:
            if person.available == False:
                counter+=1
        if counter > (len(team)/2):
            return "Too many members of the team are on leave already, sorry!"
        if employee.holiday_days_remaining < days:
            return "You dont have enough holiday days."
        employee.hours_worked+= days* 8
        employee.holiday_days_remaining -= days
        employee.available = False
        return "Approved, have fun!"
    
    def pay_workers(self):
        for team in (self.sales_team,self.engineering_team):
            for employee in team:
                hourly_rate = employee.salary / 170
                print(f"{employee.name}:\n {employee.hours_worked * hourly_rate}$ for {employee.hours_worked} hours worked.")
                print(f"{employee.overtime_hours*(hourly_rate*1.5)}$ for {employee.overtime_hours} hours of overtime.")
                employee.hours_worked=0
                employee.overtime_hours = 0
        self.sales.clear()
        self.progress.clear()
    def show_all_reports(self):
        print("Sales (name,sales,money):")
        print(self.sales)
        print(f"---------------------\nEngineering Progress (name,description):\n{self.progress}")

manager = Manager("sefu")
sales2 = Salesperson("sandu",manager)
sales1 = Salesperson("sebi",manager)
sales3 = Salesperson("sales3",manager)
eng1 = Engineer("emi",manager)
eng2 = Engineer("gigi",manager)

sales1.work_report(7,5,200)
sales2.work_report(10,6,300)
sales2.work_report(8,2,100)
sales1.work_report(9,1,50)

eng1.work_report(8,"2 buguri fixate, mai am")
eng2.work_report(8,"am schimbat culoarea la 2 butoane")
eng1.work_report(10,"am citit documentatia")

manager.show_all_reports()

sales1.request_vacation(2)
sales1.available= True
sales1.request_vacation(10)
sales1.request_vacation(1)
sales1.available= True

manager.pay_workers()

#5 Create a class hierarchy for animals, starting with a base class Animal. Then, create subclasses like Mammal, Bird, and Fish. Add properties and methods to represent characteristics unique to each animal group.
print("\n#5")
class Animal:
    def __init__(self,name,habitat,diet):
        self.name = name
        self.habitat = habitat
        self.diet = diet
class Mammal(Animal):
    def __init__(self,name,habitat,diet,nr_of_legs,fur_color):
        super().__init__(name,habitat,diet)
        self.nr_of_legs=nr_of_legs
        self.fur_color=fur_color
    def give_birth(self):
        print(f"The {self.name} gave birth")
    def __str__(self):
        return f"The {self.name} is a {self.diet} mammal, with {self.nr_of_legs} legs and {self.fur_color} fur. It`s habitat: {self.habitat}"
class Bird(Animal):
    def __init__(self,name,habitat,diet,feather_color):
        super().__init__(name,habitat,diet)
        self.feather_color = feather_color
    def fly(self):
        print(f"The {self.name} started flying.")
    def lay_eggs(self):
        print(f"The {self.name} lays eggs")
    def __str__(self):
        return f"The {self.name} is a {self.diet} bird, with {self.feather_color} feathers. It`s habitat: {self.habitat}"
class Fish(Animal):
    def __init__(self,name,habitat,diet,color):
        super().__init__(name,habitat,diet)
        self.color = color

    def breath_underwater(self):
        print(f"The {self.name} can breathe underwater")

    def __str__(self):
        return f"The {self.name} is a {self.diet} fish, with {self.color} scales. It`s habitat: {self.habitat}"

bird = Bird("eagle","mountains","carnivore","brown and grey")
mammal = Mammal("cow","plains","herbivore",4,"black and white")
fish = Fish("Catfish","river","omnivore","white and silver")

bird.fly()
bird.lay_eggs()
print(bird)

mammal.give_birth()
print(mammal)

fish.breath_underwater()
print(fish)

#6 Design a library catalog system with a base class LibraryItem and subclasses for different types of items like Book, DVD, and Magazine. Include methods to check out, return, and display information about each item.
print("\n#6")
from datetime import datetime, timedelta

class LibraryItem:
    def __init__ (self, element_id, name):
        self.element_id=element_id
        self.name = name
        self.status_checked_out = False
        self.due_date = None

    def check_out(self, period_of_time=30):
        if not self.status_checked_out:
            self.status_checked_out = True
            self.due_date = datetime.now() + timedelta(days=period_of_time)
            print(f"The item {self.name} has been checked out.")
        else:
            print(f"The item {self.name} is already checked out, until {self.due_date}.")

    def return_item(self):
        if self.status_checked_out:
            self.status_checked_out = False
            self.due_date = None
            print(f"The item {self.name} was returned successfully.")
        else:
            print(f"The item {self.name} was not checked out.")

    def display_info(self):
        status = "Available" if not self.status_checked_out else f"Unavailable, until {self.due_date}"
        print(f"The item with the ID {self.element_id} and the name {self.name} is {status}")


class Book(LibraryItem):
    def __init__(self, element_id, name, author, nr_of_pages, genre):
        super().__init__(element_id, name)
        self.author=author
        self.nr_of_pages=nr_of_pages
        self.genre=genre

    def display_info(self):
        super().display_info()
        print(f"The author is {self.author}, the book has {self.nr_of_pages} pages, and it has the genre {self.genre}")


class DVD(LibraryItem):
    def __init__(self, element_id, name, material, capacity):
        super().__init__(element_id, name)
        self.material=material
        self.capacity=capacity

    def display_info(self):
        super().display_info()
        print(f"The DVD's material is {self.material} and it has a capacity of {self.capacity} KB")


class Magazine(LibraryItem):
    def __init__(self, element_id, name, nr_of_pages, domain):
        super().__init__(element_id, name)
        self.nr_of_pages=nr_of_pages
        self.domain=domain

    def display_info(self):
         super().display_info()
         print(f"The magazine's domain is {self.domain} and it has {self.nr_of_pages} pages.")



book1 = Book(1, "Capra cu trei iezi", "Ion Creanga", 50, "Horror")
book1.display_info()
book1.check_out(15)
book1.display_info()
book1.return_item()
book1.display_info()
print("----------------------------------------")

dvd1 = DVD(2, "Gica Petrecu", "plastic", 10)
dvd1.display_info()
dvd1.check_out()
dvd1.display_info()
dvd1.return_item()
dvd1.display_info()
print("----------------------------------------")

magazine1 = Magazine(3, "Terra", 20, "Geography")
magazine1.display_info()
magazine1.check_out()
magazine1.display_info()
magazine1.return_item()
magazine1.display_info()


    