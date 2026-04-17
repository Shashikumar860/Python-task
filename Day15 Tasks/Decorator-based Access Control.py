dic={
    "praveen":"python developer",
    "charan":"employee"
}
def access_control(role):
    def decorator(func):
        def wrapper(name):
            if dic.get(name)==role:
                print("Accessed")
                return func(name)
            else:
                print("Denied")
        return wrapper
    return decorator
@access_control("python developer")
def developer(name):
    print(f"{name} is a python developer")
@access_control("employee")
def employee(name):
    print(f"{name} is a employee")
@access_control("Hacker")
def Hacker(name):
    print(f"{name} is a Hacker")
developer("praveen")
employee("charan")
Hacker("praveen")
Hacker("Name")