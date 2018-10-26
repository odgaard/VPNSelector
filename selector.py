import requests
import re
import math

import time
import random
import struct
import select
import socket

def run():
	download_link = "https://privatevpn.com/serverlist/"
	page = requests.get(download_link)
	urls = re.findall("<td>\s(.+\.privatevpn\.com)\s</td>", page.text)
	url_time = []
	for res in urls:
		res = res.strip()
		print(res)
		try:
			p = float(ping(res))
			url_time.append((p, res))
		except:
			pass
	url_time.sort()
	min_time = url_time[0][0] 
	
	for (p, res) in url_time:
		p_in_ms = math.ceil(p*1000)
		x_p = math.ceil(p/min_time) 
		print("Ping: " + str(p_in_ms) + "ms, " + str(x_p)+"x, URL: " + res)
		

#	names = re.findall("<td>(.*)</td>", page.text)
#	print(names)	
#	for res in names:
#		print(res)
	



def chk(data):
    x = sum(x << 8 if i % 2 else x for i, x in enumerate(data)) & 0xFFFFFFFF
    x = (x >> 16) + (x & 0xFFFF)
    x = (x >> 16) + (x & 0xFFFF)
    return struct.pack('<H', ~x & 0xFFFF)


def ping(addr, timeout=1, number=1, data=b''):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as conn:
        payload = struct.pack('!HH', random.randrange(0, 65536), number) + data

        conn.connect((addr, 80))
        conn.sendall(b'\x08\0' + chk(b'\x08\0\0\0' + payload) + payload)
        start = time.time()

        while select.select([conn], [], [], max(0, start + timeout - time.time()))[0]:
            data = conn.recv(65536)
            if len(data) < 20 or len(data) < struct.unpack_from('!xxH', data)[0]:
                continue
            if data[20:] == b'\0\0' + chk(b'\0\0\0\0' + payload) + payload:
                return time.time() - start
run()
