# IS496: Computer Networks (Spring 2022)
# Programming Assignment 2 - Starter Code
# Name and NetId of each member:
# Member 1: River Liu, ll24
# Member 2: Yuxuan Jiang, yj26
# Member 3: Zhizhou Xu, zhizhou6

# Note: 
# This starter code is optional. Feel free to develop your own solution to Part 1. 
# The finished code for Part 1 can also be used for Part 2 of this assignment. 


# Import any necessary libraries below
import socket, sys, struct


############## Beginning of Part 1 ##############
# define a buffer size for the message to be read from the TCP socket
BUFFER = 1024


def init_sock(host, port):
    sin = (host, port)

    # create a datagram socket for TCP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # connect to the server
    try:
        sock.connect(sin)
    except socket.error:
        print('Failed to connect.')
        sys.exit()

    return sock


def part1 ():
    # fill in the hostname and port number
    hostname = 'student00.ischool.illinois.edu'
    port = 41022

    # A dummy message (in bytes) to test the code
    message = b'Hello World'

    # convert the host name to the corresponding IP address
    host = socket.gethostbyname(hostname)
    sock = init_sock(host, port)

    # send the message to the server
    sock.send(message)

    # receive the acknowledgement from the server
    acknowledgement = struct.unpack('i', sock.recv(BUFFER))[0]

    # print the acknowledgement to the screen
    print(f'Acknowledgement: {acknowledgement}')

    # close the socket
    sock.close()


############## End of Part 1 ##############




############## Beginning of Part 2 ##############


# List all the files and directories in server directory
def ls(sock):
    print(sock.recv(BUFFER).decode('utf-8'))


# Main function for Part 2
def part2 ():
    print("********** PART 2 **********")

    # fill in the hostname and port number
    hostname = sys.argv[1]
    port = int(sys.argv[2])

    # convert the host name to the corresponding IP address
    try:
        host = socket.gethostbyname(hostname)
    except socket.error:
        print('Failed to resolve hostname.')
        sys.exit()

    # Initiate the socket and connect to the server
    sock = init_sock(host, port)
    print('Connection established')

    while True:
        # Waiting for user to prompt command
        command = input('> ')
        command_byte = command.encode('utf-8')

        # Send the command to the server in byte
        sock.send(command_byte)

        # According to the command, print different results.
        if command == 'LS':
            ls(sock)
        elif command == 'QUIT':
            sock.close()
            break


############## End of Part 2 ##############


if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input. 
    # Otherwise, it will go with function part2() to handle the command line input 
    # as specified in the assignment instruction. 
    if len(sys.argv) == 1:
        part1()
    else:
        part2()

   