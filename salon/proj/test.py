# #inheritance
# class Person():
#     def __init__(self, name, no):
#         self.name=name
#         self.no=no

#     def display(self):
#         print(self.name)
#         print(self.no)
#     def details(self):
#         print(self.name)
#         print(self.no)



# class Inh(Person):
#     def __init__(self, name, no, sal, age):
#         self.sal=sal
#         self.age=age
#         super().__init__(name, no)   

#     def details(self):
#         print(self.name)         
#         print(self.no)                
#         print(self.age)                
#         print(self.sal)                

# obj=Inh("m",1, 25, 41)
# obj.display()
# obj.details()      


# class Vehicle():
#     pass

# class Bus(Vehicle):
#     def __init__(self):
#        pass

# class vehicle:
# 	def __init__(self,name ,max_speed,mileage):
# 		self.name = name
# 		self.max_speed = max_speed
# 		self.mileage = mileage
		

# class bus(vehicle):
# 	def print(self):
# 		print("vehicle Name:",self.name)
# 		print("vehicle speed:",self.max_speed)
# 		print("vehicle mileage:",self.mileage)

# b = bus("school volve",180,12)
# b.print()
# class A():
#     pass

# class Vehicle():

#     pass



# class Bus(Vehicle):

#     def __init__(self, name, color):

# class Parent:
#   def __init__(self, txt):
#     self.message = txt

#   def printmessage(self):
#     print(self.message)

# class Child(Parent):
#   def __init__(self, txt):
#     super().__init__(txt)

# x = Child("Hello, and welcome!")

# x.printmessage()       

class Vehicle:
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage
 
    def seating_capacity(self, capacity):
        return f"The seating capacity of a {self.name} is {capacity} passengers"

class Bus(Vehicle):
    def __init__(self, name, max_speed, mileage):
        super().__init__(name, max_speed, mileage)
    


a=Bus("school bus",1,2)
print(a.seating_capacity(50))


