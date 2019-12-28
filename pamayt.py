import requests, hashlib, base64, json, pprint
import urllib.parse 

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
family = 'попов'
s = requests.Session()
url = 'https://pamyat-naroda.ru/'
# Первый запрос - получаем 307 статус
res = requests.get(url, allow_redirects=False)
if(res.status_code==307):
    print('*********************')
    print(res.status_code)
    #for item in res.cookies.items():
    #    print(item)
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
    #######################################
    if(res1.status_code==200):
        print('*******************')
        print(res1.status_code)
        print(res1.cookies[str_00])
        #pprint.pprint(res1.cookies)
        #for item in res1.cookies.items():
        #    print(item)
        
        cookies = parse_json_file('cookie_3_4.txt')
        cookies[str_00] = res1.cookies[str_00]
        cookies[str_0b] = res.cookies[str_0b]
        cookies[str_PNSESSIONID] = res.cookies[str_PNSESSIONID]
        cookies['r'] = res.cookies[str_0b]
        
        headers = parse_file('header_3_4.txt')
        headers['Cookie'] = make_str_cookie(cookies)
        headers['Content-Type'] = 'application/json'

        ############## 3-й запрос #############
        url3 = 'https://pamyat-naroda.ru/heroes/?last_name='+urllib.parse.quote(family)+'&first_name=&middle_name=&date_birth=&adv_search=y'
        res3 = requests.get(url3,headers=headers,cookies=cookies)
        print("************************")
        print(res3.status_code)
        #for item in res3.cookies.items():
        #    print(item)
        print(res3.cookies[str_00])

        ############## 4-й запрос #############
        headers=parse_file('header_search.txt')
        #headers['Content-Type'] = 'application/json; charset=UTF-8'
        headers['Referer'] = 'https://pamyat-naroda.ru/heroes/?last_name='+urllib.parse.quote(family)+'&first_name=&middle_name=&date_birth=&adv_search=y'

        bs = res3.cookies[str_00]
        bs += "=" * ((4 - len(res3.cookies[str_00]) % 4) % 4)
        bs = base64.b64decode(bs).decode()
        a_bs = bs.split('XXXXXX')[0]
        b_bs = bs.split('XXXXXX')[1].split('YYYYYY')[0]
        print(a_bs)
        print(b_bs)
        data = {"query":{"bool":{"should":[{"bool":{"should":[{"match":{"last_name":{"query":"попов","boost":6}}},{"match":{"last_name":{"query":"попов","operator":"and","boost":7}}},{"match":{"last_name":{"query":"попов","analyzer":"standard","boost":9}}},{"match":{"last_name":{"query":"попов","analyzer":"standard","operator":"and","boost":10}}},{"match":{"last_name":{"query":"попов","analyzer":"standard","fuzziness":2}}}]}}],"minimum_should_match":1}},"indices_boost":[{"memorial":1},{"podvig":2},{"pamyat":3}],"size":"20","from":0}
        #data = {k: quote(str(v)) for k,v in data.items()}
        #data = quote(data.decode())
        #print(data)

        url4 = 'https://cdn.pamyat-naroda.ru/data/'+a_bs+'/'+b_bs+'/memorial,podvig,pamyat/chelovek_vpp,chelovek_donesenie,vspomogatelnoe_donesenie,chelovek_gospital,chelovek_dopolnitelnoe_donesenie,chelovek_zahoronenie,chelovek_eksgumatsiya,chelovek_plen,chelovek_prikaz,chelovek_kartoteka_memorial,chelovek_nagrazhdenie,chelovek_predstavlenie,chelovek_kartoteka,chelovek_yubileinaya_kartoteka,commander,/_search'
        #url4 = 'https://cdn.pamyat-naroda.ru/data/xfT3_ZDUZaEaEHP3aW_rTA/1577394133/memorial,podvig,pamyat/chelovek_vpp,chelovek_donesenie,vspomogatelnoe_donesenie,chelovek_gospital,chelovek_dopolnitelnoe_donesenie,chelovek_zahoronenie,chelovek_eksgumatsiya,chelovek_plen,chelovek_prikaz,chelovek_kartoteka_memorial,chelovek_nagrazhdenie,chelovek_predstavlenie,chelovek_kartoteka,chelovek_yubileinaya_kartoteka,commander,/_search'

        print(url4)
        res4 = requests.post(url4,data=json.dumps(data),headers=headers)
        data = json.loads(res4.text)
        hits = data['hits']['hits']
        print(type(hits[0]))
        for key, value in hits[0].items():
            print (key, value)
        ###############################
        #
        ###############################

        exit(0)



