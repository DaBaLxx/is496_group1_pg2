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
import socket, sys, struct, time, subprocess


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
    port = 41029

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


def dn(sock, command):

    # get file size from server and file name from command
    file_size = struct.unpack('i', sock.recv(BUFFER))[0]
    filename = command[3:]

    # file exists on server side
    if file_size != -1:

        f = open(filename, 'wb')
        recv_size = 0

        # start time
        start = time.time()

        # receiving file
        while recv_size < file_size:
            data = sock.recv(BUFFER)
            f.write(data)
            recv_size += len(data)

        # end time
        end = time.time()

        # speed
        speed = round(recv_size / 1000000 / (end - start), 2)

        # print throughput
        print('{} bytes have been transfered in {} seconds: {} Megabytes/second'.format(recv_size, round(end-start, 6), speed))
    
    # file does not exist on server side
    else:
        print('File does not exist!')


def up(sock, command):
    filename = command[3:]

    # check if the file exists and send ackowledgement to client
    result = subprocess.run(['ls', '-l', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # file exists
    if result.stdout:

        # send a confirmation to server
        sock.send(struct.pack('i', 1))

        # send file name to server
        sock.send(filename.encode('utf-8'))

        # receive ackowledgement from server
        acknowledgement = struct.unpack('i', sock.recv(BUFFER))[0]

        # get the size of this file
        file_size = int(result.stdout.decode('utf-8').split(' ')[4])

        # file does not exist on server side
        if acknowledgement == -1:

            # send file size to server
            sock.send(struct.pack('i', file_size))

            # send file
            with open(filename, 'rb') as f:
                for line in f:
                    sock.send(line)
            
            # print throughput
            throughput = sock.recv(BUFFER).decode('utf-8')
            print(throughput)
        
        # file exists on server side
        else:

            # ask user if to overwrite the file
            confirm = input('File already exists. Do you want to overwrite the original file? ')
            confirm = confirm.lower()

            if confirm == 'no':

                # send a negative confirmation to server
                sock.send(struct.pack('i', -1))
                print('Upload abandoned by user.')

            elif confirm == 'yes':

                # send file size to server
                sock.send(struct.pack('i', file_size))
                
                # send file
                with open(filename, 'rb') as f:
                    for line in f:
                        sock.send(line)
                
                # print throughput
                throughput = sock.recv(BUFFER).decode('utf-8')
                print(throughput)
            
            else:
                # send a negative confirmation to server
                sock.send(struct.pack('i', -1))
                print('Failed to resolve command.')
    
    # file does not exists
    if result.stderr:

        # send a negative confirmation to server
        sock.send(struct.pack('i', -1))
        print('File does not exist!')


def rm(sock, command):
    # check if the file exists
    acknowledgement = struct.unpack('i', sock.recv(BUFFER))[0]
    
    # file exists
    if acknowledgement == 1:
        # ask user delete the file or not
        confirm = input('Are you sure? ')
        confirm = confirm.lower()

        # send confirmation to server
        sock.send(confirm.encode('utf-8'))

        if confirm == 'yes':

            # acknowlegement from server
            delete = struct.unpack('i', sock.recv(BUFFER))[0]

            # delete successfully
            if delete == 1:
                print('File deleted!')

            # delete unsuccessfully
            else:
                print('Unable to delete the file!')
        else:
            print('Delete abandoned by user.')
    
    # file does not exist
    else:
        print('File does not exist!')



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
        elif command[:2] == 'DN':
            dn(sock, command)
        elif command[:2] == 'UP':
            up(sock, command)
        elif command[:2] == 'RM':
            rm(sock, command)
        else:
            print('Failed to resolve command.')


############## End of Part 2 ##############


if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input. 
    # Otherwise, it will go with function part2() to handle the command line input 
    # as specified in the assignment instruction. 
    if len(sys.argv) == 1:
        part1()
    else:
        part2()

   