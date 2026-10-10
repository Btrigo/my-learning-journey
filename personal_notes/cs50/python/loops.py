#def main():
 #   print_row(4)

#def print_row(n):
 #   print("#" * n)

#main()


#def main():
 #   print_square(4)

#def print_square(n):
#for each row in square
    #for i in range(n):
# for each brick in row
#        for j in range(4):
# print brick
#            print("#", end="")
#        print()

#main()


def main():
    print_square(4)

def print_square(size):
    for i in range(size):
        print_row(size)

def print_row(width):
    print("#" * width)


main()