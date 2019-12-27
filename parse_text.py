import base64, hashlib,json
import urllib.parse

s='a1Q1Nmh0TXVIVVdOLVBWU0hhU0ZGd1hYWFhYWDE1Nzc0NDUwOTdZWVlZWVlYVXZMaDhFdUlHTDd2a1NLeUFfRXZnWFhYWFhYMTU3NzQ0ODY5N1lZWVlZWQ'
s += "=" * ((4 - len(s) % 4) % 4)
bs = s
bs = base64.b64decode(bs).decode()
a_bs = bs.split('XXXXXX')[0]
b_bs = bs.split('XXXXXX')[1].split('YYYYYY')[0]
print(a_bs)
print(b_bs)
#kT56htMuHUWN-PVSHaSFFw/1577445097
g='попов'
#print(urllib.quote(g.decode('utf-8')))
print(urllib.parse.quote(g))
#D0%BF%D0%BE%D0%BF%D0%BE%D0%B2