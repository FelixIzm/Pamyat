import base64, hashlib

s = """Host: pamyat-naroda.ru
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: */*
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 22
Connection: keep-alive
Referer: https://pamyat-naroda.ru/
Cookie: _ga=GA1.2.770534896.1577099369; _ym_uid=15770993691007649153; _ym_d=1577099369; BX_USER_ID=4107cb9ed160b6220db33d1655cfd055; BITRIX_PN_DATALINE_LNG=ru; _gid=GA1.2.1148472317.1577267427; _ym_isad=2; PNSESSIONID=Ir4ZjA2VvabI8PLeDnyxaH8hK2t4xnb4; bda88568a54f922fcdfc6dbf940e5d00=TXlFdUJDcjQtbE96MFRQTHJfc1NDQVhYWFhYWDE1NzczNjA1NTlZWVlZWVlnQlVfNGx3T0RBdjgxS0htU3VyY3h3WFhYWFhYMTU3NzM2NDE1OVlZWVlZWQ; 56105c9ab348522591eea18fbe4d080b=792af96f5e174474907798b6b4a6baf7; r=792af96f5e174474907798b6b4a6baf7
TE: Trailers"""

def parse_file (name_file):
    f = open(name_file, 'r')
    s = f.read()
    dict_={}
    list_ = s.splitlines()
    for item in list_:
        items = item.split(":")
        dict_[items[0]] = items[1].lstrip() 
    return dict_

#print(parse_file('header_0.txt'))

s1='ZUgzZklKeFFyUWNfb1FFX1R1d0Vtd1hYWFhYWDE1NzczNjc2NzJZWVlZWVlmN1lZNzZfNWZKLW4xR0JUdTJ3cW53WFhYWFhYMTU3NzM3MTI3MllZWVlZWQ'

#s += "=" * ((4 - len(s) % 4) % 4)
#print(s1)
s3='idBDkFY6IzsNAhe792af96f5e174474907798b6b4a6baf7x7hDwqbFHpAaXcUSy'
s4= '4107cb9ed160b6220db33d1655cfd055'
r ='792af96f5e174474907798b6b4a6baf7'

s = r+s4+s3
s = r+"db76xdlrtxcxcghn7yusxjcdxsbtq1hnicnaspohh5tzbtgqjixzc5nmhybeh"

ddd='83153a0eaa52d09d47a9274bfcb8efcd'
#bs = base64.b64decode(s).decode()
#print(bs)
print(hashlib.md5(s.encode('utf-8')).hexdigest())