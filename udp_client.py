import socket
import sys
import datetime

def setup():
    try:
        sys.argv[1]
    except IndexError:
        HOST = raw_input("Enter HOST:\n>>")
        if HOST == '':
            HOST = 'localhost'

    else:
        HOST = sys.argv[1]

    print('Host "{}" selected'.format(HOST))
    return HOST

#------------------------------------------------------------------------------------------------------------

def display():
    print '\n\nItem ID       Item Description'
    print '______________________________\n'
    for item,descriptions in zip(item_id,item_des):
        print item,'________',descriptions

#------------------------------------------------------------------------------------------------------------

def selectItem():
    itemFound = False
    request_id =''
    userChoice = raw_input("Enter Item ID to get details:\n>>")
    while not itemFound:
        if userChoice in item_id:
            request_id = userChoice
            itemFound = True
        else:
            userChoice = raw_input("Item not found! Try again: ")
    else:
            print '\nItem {} Found! Getting details...\n'.format(request_id)
            return request_id

#------------------------------------------------------------------------------------------------------------

def serverRequest(request_id):
     currentTime = str(datetime.datetime.now().time()).split('.')
     timeSent = currentTime[1]
     data = request_id
     my_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     my_socket.settimeout(10)
     try:
         my_socket.sendto(data,0, (HOST,PORT))
         received = my_socket.recv(1024)
     except socket.timeout:
         print('Connection timed out.')
         return
     currentTime = str(datetime.datetime.now().time()).split('.')
     timeRec = currentTime[1]
     RTT = int(timeRec)-int(timeSent)
     received = received.split(';')


     print 'Item ID\t\tItem Description\t\tUnit Price\t\tInventory\t\tRTT of Query'
     print '------\t\t---------------\t\t\t----------\t\t---------\t\t------------'
     print received[0]+'\t\t'+received[1]+(' '*(25-len(received[1])))+received[2]+'\t\t\t'+received[3]+'\t\t\t\t'+str(RTT)+' ms'
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

PORT = 5120
data = ''
item_id = ['00001','00002','00003','00004','00005','00006']
item_des = ['New Inspiron 15','New Inspiron 17','New Inspiron 15R',
            'New Inspiron 15z Ultrabook','XPS 14 Ultrabook','New XPS 12 UltrabookXPS']




HOST = setup()
keepGoing = True
while keepGoing:
    display()
    request_id = selectItem()
    serverRequest(request_id)
    userChoice = raw_input('\nWould you like to check another product?'
                           '\nPress any key to continue or q to quit:\n>>')
    if userChoice.lower() == 'q':
        print "\n\nSee ya!"
        keepGoing = False