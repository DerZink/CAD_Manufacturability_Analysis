import time

# to be used for genrating part's id 
def generateid():
    id_gen=int(round(time.time()*1000))
    time.sleep(0.00000001)
    return id_gen

# to be used for genrating part's creation
def generatedate():
    return str(time.ctime((time.time())))


if __name__ == "__main__":
    for i in range(1):
        print(type(generateid()))
        #generateid()