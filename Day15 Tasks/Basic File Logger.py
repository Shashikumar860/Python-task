try:
    with open("log.txt","a") as file:
        while True:
            inp=input("enter login or logout: ")
            if inp=="logout":
                break
            file.write(inp+"\n")
except FileNotFoundError as f:
    print("file not found",f)
except Exception as e:
    print("exception occured",e)