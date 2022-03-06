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
import os, socket, sys, struct, subprocess, time


############## Beginning of Part 1 ##############
# Define a buffer size for the message to be read from the TCP socket
BUFFER = 1024


def init_sock(host, port):
    sin = (host, port)

    # Create a datagram socket for TCP
    try:
        # sycn success twice
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # Bind the socket to address
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(sin)
    except socket.error:
        print('Failed to bind socket.')
        sys.exit()

    # Start listening
    try:
        sock.listen()
    except socket.error:
        print('Failed to listen.')
        sys.exit()

    # Accept the connection and record the address of the client socket
    try:
        conn, addr = sock.accept()
    except socket.error:
        print('Failed to accept.')
        sys.exit()

    return sock, conn, addr


def part1 ():
    print("********** PART 1 **********")
    # Fill in the IP address of the host and the port number
    host = '192.17.61.22'
    port = 41029
    sock, conn, addr = init_sock(host, port)

    # Receive message from the client
    data = conn.recv(BUFFER)

    # Print the message to the screen
    print('Client Message: ' + data.decode('utf-8'))

    # Send an acknowledgement (e.g., integer of 1) to the client
    conn.send(struct.pack('i', 1))

    # Close the socket
    sock.close()


############## End of Part 1 ##############




############## Beginning of Part 2 ##############


def ls(conn):
    # Use the shell command 'ls -l' to list the directory at the server, and record the result
    result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)

    # Send the result back to the client
    conn.send(result.stdout)


def dn(conn, command):

    # get file name from command
    filename = command[3:]

    # check if file exists
    result = subprocess.run(['ls', '-l', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    # file exists
    if result.stdout:

        # get file size and send it to client
        file_size = int(result.stdout.decode('utf-8').split(' ')[4])
        conn.send(struct.pack('i', file_size))

        # send file
        with open(filename, 'rb') as f:
            for line in f:
                conn.send(line)
    
    # file does not exist
    if result.stderr:
        conn.send(struct.pack('i', -1)) 


def up(conn):

    # ackowledgement from client
    acknowledgement = struct.unpack('i', conn.recv(BUFFER))[0]

    # file exists on client side
    if acknowledgement == 1:

        # receive file name from client
        filename = conn.recv(BUFFER).decode('utf-8')

        # check if the file already exists
        result = subprocess.run(['ls', '-l', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # file exists
        if result.stdout:
            # send acknowledgement to client
            conn.send(struct.pack('i', 1))
        # file does not exists
        if result.stderr:
            conn.send(struct.pack('i', -1))

        # receive file size from client
        file_size = struct.unpack('i', conn.recv(BUFFER))[0]

        if file_size != -1:

            f = open(filename, 'wb')
            recv_size = 0

            # start time
            start = time.time()

            # receiving file
            while recv_size < file_size:
                data = conn.recv(BUFFER)
                f.write(data)
                recv_size += len(data)

            # end time
            end = time.time()

            # speed
            speed = round(recv_size / 1000000 / (end - start), 4)

            # compute the throughput and send it to client
            throughput = '{} bytes have been transfered in {} seconds: {} Megabytes/second'.format(recv_size, round(end-start, 6), speed)
            conn.send(throughput.encode('utf-8'))


def rm(conn, command):
    filename = command[3:]
    # check if the file exists and send ackowledgement to client
    result = subprocess.run(['ls', '-l', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # file exists
    if result.stdout:
        conn.send(struct.pack('i', 1))

        # get the confirmation from client
        confirm = conn.recv(BUFFER).decode('utf-8')
        if confirm == 'yes':
            delete = subprocess.run(['rm', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # delete unsuccessfully
            if delete.stderr:
                conn.send(struct.pack('i', -1))
            # delete successfully
            else:
                conn.send(struct.pack('i', 1))

    # file does not exist
    if result.stderr:
        conn.send(struct.pack('i', -1))


# Main function for Part 2
def part2 ():
    print("********** PART 2 **********")
    # Fill in the IP address of the host and the port number
    host = '192.17.61.22'
    port = int(sys.argv[1])

    while True:
        print(f'Waiting for connections on port {port}')
        try:
            # Establish the connection with the client
            sock, conn, addr = init_sock(host, port)
            print('Connection established.')

            while True:
                # Receive the command from client
                data = conn.recv(BUFFER)
                command = data.decode('utf-8')

                # According to the command, execute certain function
                if command == 'LS':
                    ls(conn)
                elif command == 'QUIT':
                    sock.close()
                    break
                elif command[:2] == 'DN':
                    dn(conn, command)
                elif command[:2] == 'UP':
                    up(conn)
                elif command[:2] == 'RM':
                    rm(conn, command)
                else:
                    print('Failed to resolve command.')

        # Use Ctrl+C to shut down the server
        except KeyboardInterrupt:
            print('Server Shutdown.')
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




