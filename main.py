import subprocess
from query_data import query_rag

def query_model(query):
    response = query_rag(query)
    return response

running = True
initial = True

subprocess.run(["python", "populate_database.py"])
while running:
    while initial:
        query = str(input("What would you like to ask? "))
        initial = False
        query_model(query)
        print("\n")

    continue_ = str(input("Is there anything else you want to know? ")).lower()

    if continue_ == "n" or continue_ == "no":
        print("Good bye")
        running = False

    elif continue_ == "y" or continue_ == "yes":
        query = str(input("What would you like to ask again? "))
        query_model(query)
        print("\n")

    else:
        query_model(continue_)
        print("\n")



