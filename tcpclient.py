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
import socket
import sys


############## Beginning of Part 1 ##############
# TODO: define a buffer size for the message to be read from the TCP socket
BUFFER = 4096

def part1 ():
    # TODO: fill in the hostname and port number
    hostname = 'student00.ischool.illinois.edu'
    port = 41022

    # A dummy message (in bytes) to test the code
    message = b'Hello World'

    # TODO: convert the host name to the corresponding IP address
    host = socket.gethostbyname(hostname)
    sin = (host, port)

    # TODO: create a datagram socket for TCP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # TODO: connect to the server
    try:
        sock.connect(sin)
    except socket.error:
        print('Failed to connect.')
        sys.exit()

    # TODO: send the message to the server
    sock.send(message)

    # TODO: receive the acknowledgement from the server
    data = sock.recv(BUFFER)
    acknowledgement = int.from_bytes(data, 'big')

    # TODO: print the acknowledgement to the screen
    print(f'Acknowledgement: {acknowledgement}')

    # TODO: close the socket
    sock.close()


############## End of Part 1 ##############




############## Beginning of Part 2 ##############


# main function for Part 2
# def part2 ():



############## End of Part 2 ##############


if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input. 
    # Otherwise, it will go with function part2() to handle the command line input 
    # as specified in the assignment instruction. 
    if len(sys.argv) == 1:
        part1()
    else:
        part2()

   