import logging
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.filesystems import UnixFilesystem
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from Tkinter import Tk
from tkFileDialog import askopenfilename
import netifaces
import socket
import nmap
from ftplib import FTP
import string
import os

class MyHandler(FTPHandler):

    def on_connect(self):
        print "%s:%s connected" % (self.remote_ip, self.remote_port)

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        print (str(self.remote_ip)+" just logged in::")
        print ("File transfer is starting ....")
        pass

    def on_logout(self, username):
        # do something when user logs out
        print("Transfer complete :: Exiting...")
        exit()
        pass

    def on_file_sent(self, file):
        print ("Sent file :: " + str(file))
        pass

    def on_file_received(self, file):
        print ("Recieved file :: " + str(file))
        if( str(file.split('/')[-1]) == 'cON_info_2121.txt'):
            file_r = open('cON_info_2121.txt','r')
            flnme = file_r.readline()
            flsze = file_r.readline()
            flsze = float(flsze)/1000000
            file_r.close()
            print("Filename :: "+flnme)
            print("File size :: "+str(flsze)+" MB")
            os.remove('cON_info_2121.txt')
        pass

    def on_incomplete_file_sent(self, file):
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)
        
def server():
    print("Enter intrface you wanna use::")
    
    #Check for the available network interfaces
    intr = netifaces.interfaces()
    a=1
    print "{:<8} {:<20}".format('$$Key','$$Interface')
    for i in intr : 
            print "{:<8} {:<20}".format(str(a), str(i))
            #print (str(a)+'.'+'  '+str(i))
            a = a+1

    facech = raw_input("Enter :: ")
    facech = int(facech)
    facech = facech - 1
    strintr = intr[facech]
    
    #User chooses the interface he/she wants to work with
    intrip = netifaces.ifaddresses(strintr)[2][0]['addr']
    print ('My system ip of intrfce:: '+strintr+' is :: '+intrip+' ')
    
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    """
      Read permissions:
         - "e" = change directory (CWD command)
         - "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
         - "r" = retrieve file from the server (RETR command)
        Write permissions:
         - "a" = append data to an existing file (APPE command)
         - "d" = delete file or directory (DELE, RMD commands)
         - "f" = rename file or directory (RNFR, RNTO commands)
         - "m" = create directory (MKD command)
         - "w" = store a file to the server (STOR, STOU commands)
         - "M" = change file mode (SITE CHMOD command
    """
    read_permissions = "elr"
    write_permissions = "adfmwM"
    authorizer.add_user('akash', 'root123', '.', perm=str(write_permissions))
    authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = MyHandler
    handler.authorizer = authorizer
    handler.abstracted_fs = UnixFilesystem
    handler.use_sendfile = True

    # Define a customized banner (string returned when client connects)
    handler.banner = "||cONMan is ready||."

    # Instantiate FTP server class and listen on X.X.X.X:2121
    address = (intrip, 2121)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    #enable logging
    #logging.basicConfig(filename='log/server_log.log', level=logging.DEBUG)

    # start ftp server
    server.serve_forever()

    #file sanitizer function
def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_')
    return filename
    
def file_access():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    return filename

def client():
    print('Choices::')

    #Check for the available network interfaces
    intr = netifaces.interfaces()
    a=1
    print "{:<8} {:<20}".format('$$Key','$$Interface')
    for i in intr : 
            print "{:<8} {:<20}".format(str(a), str(i))
            #print (str(a)+'.'+'  '+str(i))
            a = a+1

    facech = raw_input("Enter :: ")
    facech = int(facech)
    facech = facech - 1
    strintr = intr[facech]

    #User chooses the interface he/she wants to work with
    intrip = netifaces.ifaddresses(strintr)[2][0]['addr']
    print ('My system ip of intrfce:: '+strintr+' is :: '+intrip+' ')
    sip = intrip.split('.')
    sip = sip[0]+'.'+sip[1]+'.'+sip[2]+'.0/24'
    req_ip = 0
    while req_ip == 0:
        list_ip = []

        #deploying nmap
        nm = nmap.PortScanner()
        #'-pXXXX' is the port number
        js_ip = nm.scan(hosts=sip, arguments='-p2121 --open')

        for i in js_ip['scan']:
            list_ip.append(i)
                    
        a=1
        #Displaying machines where the reqd port is open
        print('cONMan running in the following ips::')
        print('Enter the index of the ip you wanna send it to:: ')
        print "{:<8} {:<20}".format('$$Index','$$local_IP')
        for i in list_ip : 
                print "{:<8} {:<20}".format(str(a), str(i))
                #print (str(a)+'.'+'  '+str(i))
                a = a+1
                
        req_ndx= raw_input("Enter reqd key or press 0 to scan again::")
        req_ip = int(req_ndx)
    req_ip = req_ip - 1
    req_ip = list_ip[req_ip]
    
    print('beginning connection to '+ str(req_ip))
    ftp = FTP()
    ftp.connect(str(req_ip),2121)
    ftp.login("akash","root123")
    
    raw_input("Choose the file you wanna send from the dialog box.... press Enter")
    
    re_filename = file_access()
    
    lo_filename = re_filename.split('/')[-1]
    flsz = os.stat(re_filename).st_size

    lo_filename = format_filename(lo_filename)
    
    #creating info file
    info_fln = 'cON_info_2121.txt'
    file_ob = open(info_fln,'w')
    file_ob.write(lo_filename+'\n')
    file_ob.write(str(flsz)+'\n')
    file_ob.close()
    
    print ("Sending file .... " + lo_filename)
    
    ftp.storbinary('STOR '+info_fln, open(info_fln, 'rb'))
    ftp.storbinary('STOR '+lo_filename, open(re_filename, 'rb'))
    
    #removing info file
    os.remove(info_fln)
    
    
    print('File sent. quitting')
    ftp.quit()
    
def main():
    print("===============================================")
    s = "         @@  C 0 |\| |\/| /-\ |\|  @@"
    s.encode('utf8')
    print(s)
    print("===============================================")
    print(">>>press 1. to send file")
    print(">>>press 2. to recieve file")
    r = raw_input("Enter :: ")
    r = (int)(r)
    if r==1 :
        client()
    elif r==2 :
        server()
        
if __name__ == '__main__':
    main()
    
    
