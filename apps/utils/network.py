import fcntl
import socket
import string
import struct


class NetworkInfo(object):
    
    # ifname: eth0
    def get_local_ipaddr(self, ifname:string):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])