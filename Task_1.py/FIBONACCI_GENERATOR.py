# We are making a programe that will take an input from the user and will return the fabonacci series

n = int(input("Enter the Number: "))

x = 0
y = 1
z = 0
while z < n :
    print(z)
    x = y
    y = z
    z = x + y 
    