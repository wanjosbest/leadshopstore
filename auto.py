class Vehicle:
    def __init__(self, brand, state):
        self.brand = brand
        self.state = state
    
    def move(self):
        print("ride")


class bic(Vehicle):
    def __init__(self, brand, state):
        self.brand = brand
        self.state = state
    
    def move(self):
        print("Move")

class car(Vehicle):
   pass

class plane(Vehicle):
    def __init__(self, brand, state):
        self.brand = brand
        self.state = state
    
    def move(self):
        print("fly")
        
bic1 = bic("new", "adamawa state")
car1 = car("Used", "Delta state")
plane1 = plane("new", "Borno state")

for gesture in (bic1, car1, plane1):
    print (gesture.brand)
    print (gesture.state)
    gesture.move()