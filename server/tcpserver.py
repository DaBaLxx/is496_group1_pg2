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
import os, socket, sys, struct, subprocess


############## Beginning of Part 1 ##############
# Define a buffer size for the message to be read from the TCP socket
BUFFER = 1024


def init_sock(host, port):
    sin = (host, port)

    # Create a datagram socket for TCP
    try:
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
    port = 41022
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




