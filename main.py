import random as ra
num = ra.randrange(1,10)
while True:
    num2 = int(input("enter a number : "))
    if num2>num:
        print(">")
    elif num2<num:
        print("<")
    else:
        print("the answer is true")
        break

