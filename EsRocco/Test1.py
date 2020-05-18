import string


def weight(s):
    sum = 0
    for letter in s:
        sum += string.ascii_lowercase.index(letter)

    return sum


def merges(list):

    myList = []
    for x in list:
        myList.append(x)
        myList.sort(key=weight)

    return myList


def howManyY(list):

    sum = 0

    for x in list:
        if x[-1] == "y":
            sum+=1

    return sum


list1 = ["cesare", "ces", "cesarina", "ce", "cesa", "c"]
orderedList = merges(list1)
print(orderedList)

list2 = ["segantini", "segantiny", "segoni", "segony"]
print(howManyY(list2))


def type Continent:

