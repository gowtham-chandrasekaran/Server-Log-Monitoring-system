
import sys
from datetime import datetime, timezone
from os import listdir
from os.path import isfile, join

# Global variables
ip2usage = {}

# bsearch: Performing binary search on a list of timestamps in the dictionary
# Parameters: 
# 1) values: The list of timestamps for a particular pair of IP and CPU_IDs
# 2) timestamp: The Timestamp to be searched
# Returns:
# Returns either the start or end boundary indexes containing the list of Timestamp, Usage pairs

def bsearch(values: list, timestamp: int) -> tuple:
    left, right = 0, len(values) - 1
    
    while (left <= right):
        mid = (left + right) // 2

        value = values[mid][0]
        if (value == timestamp):
            return (mid, mid)
        elif (value > timestamp):
            right = mid - 1
        else:
            left = mid + 1
    
    return (left, right)

# query: Search and display the Timestamp and usage pairs for the provided query
# Parameters: 
# 1) q: Provided query as a list
# Returns:
# None

def queryfn(q:list)->None:
    # Extracting IP and ID from query
    ip = q[1]
    id = q[2]
    print("CPU"+id+" usage on "+ip)

    # Extracting start date and start time from query
    date_start = q[3].split('-')
    time_start = q[4].split(':')

    # Conversion of start time into unix time in UTC
    dt_start = datetime(int(date_start[0]), int(date_start[1]), int(date_start[2]), int(time_start[0]), int(time_start[1]))
    utc_time = dt_start.replace(tzinfo=timezone.utc)
    s_time = utc_time.timestamp()

    # Extracting end date and end time from query
    date_end = q[5].split('-')
    time_end = q[6].split(':')

    # Conversion of end time into unix time in UTC
    dt_end = datetime(int(date_end[0]), int(date_end[1]), int(date_end[2]), int(time_end[0]), int(time_end[1]))
    utc_time = dt_end.replace(tzinfo=timezone.utc)
    e_time = utc_time.timestamp()

    # Check if required (IP,CPU_ID) pair exists in dictionary
    flag = 1
    key = (ip,id)
    if key in ip2usage:
        values = ip2usage[key]

        # Search for start index in list of values of obtained key
        start,_ = bsearch(values,s_time)

        # Search for end index in list of values of obtained key
        _,end = bsearch(values,e_time)

        # Print the obtained pairs in the desired format between the start and end index
        for i in range(start,end+1):
            if flag == 1:
                flag = 0
                print("("+datetime.utcfromtimestamp(values[i][0]).strftime("%Y-%m-%d %H:%M")+", "+str(values[i][1])+"%"+")", end="")
            else:
                print(", ("+datetime.utcfromtimestamp(values[i][0]).strftime("%Y-%m-%d %H:%M")+", "+str(values[i][1])+"%"+")", end="")
    return 


# initialise_dict: Initialise ip2usage dictionary 
# Parameters: 
# None
# Returns:
# None

def initialise_dict()->None:
    # Get directory path from command line
    path = sys.argv[1]+"/"
    # Iterate through files in directory
    for f in listdir(path):
        filepath = join(path,f)
        
        # Verify if filepath is a file
        if isfile(filepath):
            log_file = open(filepath,"r")
            print("Processing file:"+filepath)
            Lines = log_file.readlines()

            for line in Lines:
                line = line.strip()
                items = line.split('\t')
                
                # Mapping IP and CPU_IDs to corresponding timestamp and usage pairs
                if (items[1],items[2]) not in ip2usage:
                    ip2usage[(items[1],items[2])] = [(int(items[0]),int(items[3]))]
                else:
                    ip2usage[(items[1], items[2])].append((int(items[0]),int(items[3])))
            log_file.close()


def main():

    # Initialise dictionary
    print("Initialising dictionary...")
    initialise_dict()
    print("Dictionary initialised!")
    # Main loop
    while(1):
        print("\n>> ", end="")
        query = input()
        q = query.strip().split()
        if (len(q)<7 and q[0].upper() != "EXIT"):
            print("Enter a valid query!")
            continue

        if (q[0].upper() == "QUERY"):
            queryfn(q)     
        elif(q[0].upper() == "EXIT"):
            break                           

if __name__ == "__main__":
    main()