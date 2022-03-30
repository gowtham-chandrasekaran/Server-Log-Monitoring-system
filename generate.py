import random
import socket
import struct
import time
import sys
import os
from datetime import datetime

# Get the argument from command line and create a folder in that name in the present working directory
data_path = sys.argv[1]
os.mkdir(data_path)
pwd = os.getcwd() + "/"+data_path+"/"

# Create a list of 1000 random IP addresses
server_ip_addresses = []
for i in range(1000):
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    server_ip_addresses.append(ip)

# Set start timestamp and end timestamp 
# Start timestamp will be the time of execution of this program
# End timestamp will be 24 hours added to the start timestamp
timestamp = int(time.time())
start_timestamp = timestamp
end_timestamp = timestamp + (24*60*60)

# Creating a file called server_logs.txt to store usage info for one day
file1 = open(pwd + "server_logs.txt", "a")
while(timestamp <= end_timestamp):
    for i in range(1000):

        file1.write(str(timestamp)+"\t"+server_ip_addresses[i]+"\t"+str(0)+"\t"+str(random.randint(0,100))+"\n")
        file1.write(str(timestamp) + "\t" + server_ip_addresses[i] + "\t" + str(1) + "\t" + str(random.randint(0, 100))+"\n")
        ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    
    timestamp += 60
file1.close()

# Printing start and end timestamp for reference
print("Log Start Time: "+datetime.utcfromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M:%S')+" -> "+"Log End Time: "+datetime.utcfromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S'))
