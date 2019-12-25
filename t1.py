
from requests_html import HTMLSession
import json,requests, pprint, urllib.parse
import hashlib, base64

cookies = {}
headers={}

#data = {"query":{"bool":{"should":[{"bool":{"should":[{"match":{"last_name":{"query":"измайлов","boost":6}}},{"match":{"last_name":{"query":"измайлов","operator":"and","boost":7}}},{"match":{"last_name":{"query":"измайлов","analyzer":"standard","boost":9}}},{"match":{"last_name":{"query":"измайлов","analyzer":"standard","operator":"and","boost":10}}},{"match":{"last_name":{"query":"измайлов","analyzer":"standard","fuzziness":2}}}]}}],"minimum_should_match":1}},"indices_boost":[{"memorial":1},{"podvig":2},{"pamyat":3}],"size":"10","from":0}

action = "https://pamyat-naroda.ru"

r = requests.post(action)

s = "03001222bc9570cfd8bccbf270a28ec2"
result = hashlib.md5("03001222bc9570cfd8bccbf270a28ec2".encode())
print(r.cookies[result.hexdigest()])
print()
print()

cookies[result.hexdigest()]=r.cookies[result.hexdigest()]
headers['cookie']=result.hexdigest()+"="+r.cookies[result.hexdigest()]
headers['host']="pamyat-naroda.ru"
headers['referer']='https://pamyat-naroda.ru/'
action="https://pamyat-naroda.ru/heroes/?last_name=%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2&first_name=&middle_name=&date_birth=&adv_search=y"
r = requests.get(action,cookies=cookies)
#resBase64=''
resBase64 = base64.b64decode(r.cookies[result.hexdigest()]+"=")
# printing the equivalent byte value. 
#print(r.cookies)
print(resBase64.decode())
