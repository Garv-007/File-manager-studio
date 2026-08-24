from pathlib import Path
import os


def createfile():
    try:
        name = input("Please tell your file name: ")
        path =Path(name)
        if not path.exists():
            with open(path,"w") as fs:
                data = input("What you want to write :- ")
                fs.write(data)
            print("File Created succesfully")
        else:
            print("Error!! File name already existing")
    except Exception as err:
        print(f"an error occured as {err}")

def Readfile():
    try:
        name = input("Please tell your file name:- ")
        path = Path(name)
        if path.exists():
            with open(path,'r') as fs:
                content = fs.read()
                print(f"Your file is \n {content}")
        else:
            print("Error no such file exists!! ")
    except Exception as err:
        print(f"An error occured as {err}")


def updatefile():
    try:
        name = input("Please tell me your file name: ")
        path =Path(name)

        if path.exists():
            print("Operations")
            print("1. Renaming the file")
            print("2. Appedning the file")
            print("3. Overwriting a file")

            choice= int(input("Enter your options: "))

            if choice==1:
                newname=input("Tell your new file name:- ")
                new_path=Path(newname)
                if not new_path.exists():
                    path.rename(new_path)
                    print("Rename Succesffuly")
                else:
                    print("File already exists!! ")
            elif choice == 2:
                with open(path,'a')as fs:
                    data= input("what u want to append:-")
                    fs.write(" \n"+data)
                print("Succesfully Appended")
            elif choice ==3:
                with open(path,'w') as fs:
                    data= input("what u want to overwrite:-")
                    fs.write("\n"+data)
                print("Succesfully overwritten")
    except Exception as err:
        print(f"An error occured as {err}")

def deletefile():
    try:
        name = input("Please tell your file name:- ")
        path = Path(name)
        if path.exists():
            path.unlink()
            print("File deleted succesfully!!!")
        else:
            print("Error no such file exists")
    except Exception as err:
        print(f"An error occured as {err}")

while True:
    print("Press 1 for creating a file ")
    print("Press 2 for reading a file ")
    print("Press 3 for updating a file ")
    print("Press 4 for deleting a file ")
    print("Press 0 to Exit")

    a=input("Tell your Response :- ")

    if not a.isdigit():
        print("Invalid input. Please enter a number (0-4).")
        continue

    choice = int(a)

    if choice==1:
        createfile()
    elif choice==2:
        Readfile()
    elif choice==3:
        updatefile()
    elif choice==4:
        deletefile()
    elif choice == 0:  # Added Exit logic
        print("Exiting program. Goodbye!")
        break  # Stops the loop and ends the program
    else:
        print("Invalid option. Please choose 0-4.")
