#while True:
#    try:
#        x = float(input("What's x? "))
#    except ValueError:
#        print("x is not a number")
#    else:
#        break

#print(f"x is {x}")



#from fractions import Fraction

# while True:
#     try:
#         text = input("What's x? ")

#         if "/" in text:
#             numerator, denominator = text.split("/")
#             x = Fraction(numerator) / Fraction(denominator)
#         else:
#             x = Fraction(text)

#     except ValueError:
#         #print("Enter a whole number, decimal, or fraction.")
#         pass
#     except ZeroDivisionError:
#         print("Fractions with 0 in the denominator are considered \"undefined\". Please try again.")
#     else:
#         break

# print(f"x is {float(x)}")



from fractions import Fraction


def main():
    x = get_number("What's x?")
    print(f"x is {float(x)}")


def get_number(prompt):
    while True:
        try:
            text = input(prompt)

            if "/" in text:
                numerator, denominator = text.split("/")
                x = Fraction(numerator) / Fraction(denominator)
            else:
                x = Fraction(text)

        except ValueError:
            print("Enter a whole number, decimal, or fraction.")
        except ZeroDivisionError:
            print("Fractions with 0 in the denominator are \"undefined\". Please try again.")
        else:
            return x


main()