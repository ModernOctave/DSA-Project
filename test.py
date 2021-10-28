import random
t = 100
n = 11

# assign random value to k between 10 and 20
k = random.randint(10, 20)


# print the k lines each having two space seperated random integer values between 1 and n , two random unique integers value between 1 and 20 and two random unique integers value between 1 and 500
for i in range(k):
    for j in range(2):
        print(random.randint(1, n), end=' ')
    for j in range(2):
        print(random.randint(1, 20), end=' ')
    for j in range(2):
        print(random.randint(1, 500), end=' ')
    print()