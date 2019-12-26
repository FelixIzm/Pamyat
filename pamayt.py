import requests, hashlib, base64, json
cookies = {}
headers={}

str_00 = 'bda88568a54f922fcdfc6dbf940e5d00'
str_0b = '56105c9ab348522591eea18fbe4d080b'
str_PNSESSIONID = 'PNSESSIONID'

#####################################        
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
#####################################        
def parse_json_file(json_file):
    with open(json_file) as json_file:
        return json.load(json_file)
#####################################        
def make_str_cookie(cookies):
    str_cook = ''
    for key, value in cookies.items():
        str_cook += '{0}={1};'.format(key,value)
    return str_cook
#####################################        


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
    res1 = requests.get(url,cookies=cookies,headers=headers, allow_redirects=False)
    if(res1.status_code==200):
        print('*******************')
        print(res1.status_code)
        print(res1.cookies[str_00])
        exit(1)
        cookies = parse_json_file('cookie_3_4.txt')
        cookies[str_00] = res1.cookies[str_00]
        print(res1.cookies[str_0b])
        print(cookies[str_0b])
        cookies[str_0b] = res1.cookies[str_0b]
        cookies[str_PNSESSIONID] = res1.cookies[str_PNSESSIONID]
        
        headers = parse_file('header_3_4.txt')
        headers['Cookie'] = make_str_cookie(cookies)
        
        url = 'https://pamyat-naroda.ru/bitrix/templates/pn/js/build/js_libs_ext.js?b9e6e74ce868ac78a1eeea636ec0d29a'
        res2 = requests.get(url,headers=headers,cookies=cookies)
        print(res2.text)
        ###############################
        #
        ###############################
        headers={}
        headers['Host'] = 'pamyat-naroda.ru'
        headers['User-Agent'] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Connection'] = 'keep-alive'
        headers['Cookie'] = 'BITRIX_PN_DATALINE_LNG=ru;'
        headers['Upgrade-Insecure-Requests'] = '1'
        headers['Referer'] = 'https://pamyat-naroda.ru/'

        #Cookie: BITRIX_PN_DATALINE_LNG=ru; bda88568a54f922fcdfc6dbf940e5d00=d3Q1WXBGNDM5YlF5SXh1ZF9Bc2JrQVhYWFhYWDE1NzczMDQ5OTFZWVlZWVlEWUJpUXNGTGZsdGJqVHpqQVhOVHhnWFhYWFhYMTU3NzMwODU5MVlZWVlZWQ; r=792af96f5e174474907798b6b4a6baf7
        headers['Pragma'] = 'no-cache'
        headers['Cache-Control'] = 'no-cache'

        cookies={}
        cookie_00 = res1.cookies[str_00]
        cookies['BITRIX_PN_DATALINE_LNG'] = 'ru'
        cookies[str_00]=cookie_00
        cookies['r'] = res1.cookies['r']
        str_cook = ''
        for key, value in cookies.items():
            str_cook += '{0}={1};'.format(key,value)
        headers['Cookie'] = str_cook

        ############## 3-й запрос #############
        url2 = 'https://pamyat-naroda.ru/heroes/?last_name=%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2&first_name=&middle_name=&date_birth=&adv_search=y'
        res2 = requests.get(url2,cookies=cookies,headers=headers)
        print('**************')
        print(res2.cookies[str_00])
        bs = res2.cookies[str_00]
        bs += "=" * ((4 - len(res2.cookies[str_00]) % 4) % 4)
        bs = base64.b64decode(bs).decode()
        print(bs)
        a_bs = bs.split('XXXXXX')[0]
        b_bs = bs.split('XXXXXX')[1].split('YYYYYY')[0]
        print(a_bs)
        print(b_bs)
        headers={}
        headers['Host'] = 'cdn.pamyat-naroda.ru'
        headers['User-Agent'] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
        headers['Accept'] = '*/*'
        headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Connection'] = 'keep-alive'
        headers['Origin'] = 'https://pamyat-naroda.ru'
        headers['Referer'] = 'https://pamyat-naroda.ru/heroes/?last_name=%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2&first_name=&middle_name=&date_birth=&adv_search=y'
        headers['Pragma'] = 'no-cache'
        headers['Cache-Control'] = 'no-cache'
        headers['Content-Type'] = 'application/json'

        data = {"query":{"bool":{"should":[{"bool":{"should":[{"match":{"last_name":{"query":"Иванов","boost":6}}},{"match":{"last_name":{"query":"Иванов","operator":"and","boost":7}}},{"match":{"last_name":{"query":"Иванов","analyzer":"standard","boost":9}}},{"match":{"last_name":{"query":"Иванов","analyzer":"standard","operator":"and","boost":10}}},{"match":{"last_name":{"query":"Иванов","analyzer":"standard","fuzziness":2}}}]}}],"minimum_should_match":1}},"indices_boost":[{"memorial":1},{"podvig":2},{"pamyat":3}],"size":"10","from":0}
        url3 = 'https://cdn.pamyat-naroda.ru/data/'+a_bs+'/'+b_bs+'/memorial,podvig,pamyat/chelovek_vpp,chelovek_donesenie,vspomogatelnoe_donesenie,chelovek_gospital,chelovek_dopolnitelnoe_donesenie,chelovek_zahoronenie,chelovek_eksgumatsiya,chelovek_plen,chelovek_prikaz,chelovek_kartoteka_memorial,chelovek_nagrazhdenie,chelovek_predstavlenie,chelovek_kartoteka,chelovek_yubileinaya_kartoteka,commander,/_search'
        print(headers)
        res = requests.post(url3,data=data,headers=headers)
        print(res.text)
exit(1)


