#students = ["Harry Potter", "Hermione Granger", "Ron Weasley", "Draco Malfoy", "brandon trigo"]

#for i in range(len(students)):
#    print("Welcome to Hogwarts, " + students[i].title() + "!")


#students = {
 #   "Harry Potter": "Gryffindor",
  #  "Hermione Granger": "Gryffindor",
   # "Ron Weasley": "Gryffindor",
    #"Draco Malfoy": "Slytherin",
   # "Brandon Trigo": "Gryffindor"
#}

#for name, hogwarts_house in students.items():
    #print(f"Welcome to Hogwarts, {name} of {hogwarts_house}!")



students = [
    {"name": "hermione".title(), "house": "Gryffindor", "patronus": "Otter"},
    {"name": "harry".title(), "house": "Gryffindor", "patronus": "Stag"},
    {"name": "ron".title(), "house": "Gryffindor", "patronus": "Jack Russell Terrier"},
    {"name": "draco".title(), "house": "Slytherin", "patronus": None}
]

for student in students:
    print(f"Welcome to Hogwarts, {student['name']} of {student['house']}" + (f", your patronus is {student['patronus']}" if student['patronus'] else ""))
    if student['patronus']:
       print(f"Your patronus is: {student['patronus']}.")
    else:
       print("You do not have a patronus.")

 