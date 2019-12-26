import requests, hashlib, base64
cookies = {}
headers={}

str_00 = 'bda88568a54f922fcdfc6dbf940e5d00'
str_0b = '56105c9ab348522591eea18fbe4d080b'
str_PNSESSIONID = 'PNSESSIONID'

def parse_file (name_file):
    dict_ = {}
    f = open(name_file, 'r')
    s = f.read()
    dict_={}
    list_ = s.splitlines()
    for item in list_:
        items = item.split(":")
        dict_[items[0]] = items[1].lstrip() 
    return dict_

headers = parse_file('header_0.txt')
cookies = parse_file('cookie_0.txt')

s = requests.Session()
url = 'https://pamyat-naroda.ru/'
# Первый запрос - получаем 307 статус
res = requests.get(url, allow_redirects=False)
if(res.status_code==307):
    print(res.status_code)
    print(res.cookies[str_00])
    # Получили переменные из кук
    cookie_PNSESSIONID = res.cookies['PNSESSIONID']
    cookie_00 = res.cookies[str_00]
    cookie_0b = res.cookies[str_0b]
    # готовим 2-й запрос, посылаем с получанными куками
    cookies = {}
    cookies[str_00]=cookie_00
    cookies[str_0b]=cookie_0b
    cookies[str_PNSESSIONID] = cookie_PNSESSIONID
    cookies['BITRIX_PN_DATALINE_LNG'] = 'ru'
    str_cook = ''
    for key, value in cookies.items():
        str_cook += '{0}={1};'.format(key,value)
    #print(str_cook)

    headers = parse_file('header_0.txt')
    headers['Cookie'] = str_cook
    #headers['TE'] = 'Trailers'
    ############## 2-й запрос #############
    res1 = requests.get(url,cookies=cookies,headers=headers, allow_redirects=True)
    if(res1.status_code==200):
        print('*******************')
        print(res1.status_code)
        print(res1.cookies[str_00])
        #
exit(1)


