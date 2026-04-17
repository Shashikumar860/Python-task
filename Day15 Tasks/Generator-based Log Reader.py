def gen_read():
    with open("generate.txt","r") as file:
        data=file.readline()
        yield data
for i in gen_read():
    print(i)