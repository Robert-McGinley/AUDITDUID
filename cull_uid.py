#!/usr/bin/python

###########
'''
Date June 8, 2012
Author: Justin Jessup
'''
###########
'''
Disclaimer: All software provided as is. All software covered under the GPL license and free for public redistribution. 
If unintended consequences occur due to utilization of this software, user bears the resultant outcome. 
The rule of thumb is to test and validate properly all solutions prior to implementation within a production environment.
All solutions should be subject to public scruitiny, and peer review.
'''
##########

import os, subprocess, shutil
from error_handle import ConvertExceptions

# Cull the UID integer and the username string from the /etc/passwd file 
@ConvertExceptions(StandardError, 0)
def cull_uid(file_name):
    a1 = open(file_name, 'r')
    user = [ (i.split(':')[0],i.split(':')[2]) for i in a1 if "/nologin" not in i ]
    f = open("map.3.properties","a")
    f.write("event.deviceCustomNumber3,set.event.sourceUserId\n")
    [ f.write("%s,%s\n" % (i[1],i[0])) for i in user ]

# Generic function to move the map file product to the smart connector map file location
@ConvertExceptions(StandardError, 0)
def mov_map(src_path, dst_path):
    shutil.copy(src_path, dst_path)

# Generic function to zero out a file so we are starting with a clean slate with every cyclic execution of the script 
@ConvertExceptions(StandardError, 0)
def null_file(file_path):
    f = open(file_path, 'w')
    f.close()

# Generic function to check that a file exists - if the file does exist - then execute the mv_map function 
@ConvertExceptions(StandardError, 0)  
def chk_file(file_name):
    check_file = os.path.isfile(file_name)
    if(check_file == True):
        null_file(file_name)
        mov_map(src_path, dst_path)
    else: 
        mov_map(src_path, dst_path)

# Generic function - given in our use case the customer utilized Tivoli for change management control - 
# There for if a re-deployment of the Tivoli package ocurred we needed a function to ensure we starting from 
# a clean slate again. Adjust according to your use case requirements. 
@ConvertExceptions(StandardError, 0)
def rm_map(file_name):
    check_file = os.path.isfile(file_name)
    if(check_file == True):
        os.remove(file_name)
    else:
        pass

# Very simple facility to utilize the operating system tier SSH and rsync facilities for use case where the map file is generated 
# on the remote server, and you need to move the mapfile product to the remote smart connector system, specifically updating
# the map file for the remote smart connector in question. 
@ConvertExceptions(StandardError, 0)
def rsync_ssh(local_dir, remote_system, remote_dir):
    which_process = subprocess.Popen("rsync -avz -e ssh" + " " +local_dir+ " " +remote_system+ ":" +remote_dir, shell=True, stdout=subprocess.PIPE)
    which_process.stdout.close()
    which_process.wait()
    return 

# If the script is rerun via Tivoli remove any previous 
# Map file in the current working directory
map_file_name = "map.3.properties"

rm_map(map_file_name)

# Cull usernames and UID's from passwd file
passwd_file = "/etc/passwd"

cull_uid(passwd_file)

# Move the map file product from current working director to the smart connector directory
# Note this function should be utilized if the smart connector is native to the Linux system
# Otherwise comment out this section if the map file product needs to be moved to a remote smart connector     
src_path = "map.3.properties"
dst_path = "/opt/app/arcsight/sys_pipe/current/user/agent/map/map.3.properties"
file_name = "/opt/app/arcsight/sys_pipe/current/user/agent/map/map.3.properties"

chk_file(file_name)

# Method for remote update of smart connector map file
# Uncomment this section if the map file of the ArcSight smart connector to be updated resides upon a remote collection system. 
# We will simply utilize the operating system tier ssh client and rsync facility to move map file to the remote smart connector
# over writing the map file of the remote smart connector. Warning this will over write your remote map file if implemented without
# forethought 
##########
#remote_system = "username@remote_servername"
#remote_dir = "/opt/app/arcsight/sys_pipe/current/user/agent/map/map.3.properties"
#local_dir = "/current/working/directory"
# Command string rsync -avz -e ssh /home/alienone/test.txt s1:/home/ubuntu/test.txt
#rsync_ssh(remote_system, remote_dir, local_dir)