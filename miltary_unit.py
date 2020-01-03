import requests, hashlib, base64, json, pprint
import urllib.parse 
from string import Template


cookies = {}
headers={}

str_00 = 'bda88568a54f922fcdfc6dbf940e5d00'
str_0b = '56105c9ab348522591eea18fbe4d080b'
str_PNSESSIONID = 'PNSESSIONID'
military_unit = '179 габр'

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


##############################################
#    Первый запрос - получаем 307 статус     #
##############################################
headers = parse_file('mu_header1.txt')
cookies = parse_file('mu_cookie1.txt')
url = 'https://pamyat-naroda.ru/'
res1 = requests.get(url, allow_redirects=False)
if(res1.status_code==307):
    #print('*********  1  **********')
    #print(res1.status_code)
    #print(res1.cookies[str_00])
    # Получили переменные из кук
    cookie_PNSESSIONID = res1.cookies['PNSESSIONID']
    cookie_00 = res1.cookies[str_00]
    cookie_0b = res1.cookies[str_0b]
    #####################################################
    # готовим 2-й запрос, посылаем с получанными куками #
    #####################################################
    #print('')
    #print('*********  2  **********')
    cookies = {}
    cookies[str_00]=cookie_00
    cookies[str_0b]=cookie_0b
    cookies[str_PNSESSIONID] = cookie_PNSESSIONID
    cookies['BITRIX_PN_DATALINE_LNG'] = 'ru'
    headers = parse_file('mu_header2.txt')
    headers['Cookie'] = make_str_cookie(cookies)
    res2 = requests.get(url,cookies=cookies,headers=headers,allow_redirects = True)
    #######################################
    if(res2.status_code==200):
        print(res2.status_code)
        print(res2.cookies[str_00])
        ###########################################
        ##############   3-й запрос   #############
        ###########################################
        #print('')
        #print("*********  3  **********")
        cookies = parse_json_file('mu_cookie3.txt')
        cookies[str_00] = res2.cookies[str_00]
        cookies[str_0b] = res1.cookies[str_0b]
        cookies[str_PNSESSIONID] = res1.cookies[str_PNSESSIONID]
        cookies['r'] = res1.cookies[str_0b]
        headers = parse_file('mu_header3.txt')
        headers['Cookie'] = make_str_cookie(cookies)
        headers['Content-Type'] = 'application/json'

        url3 = 'https://pamyat-naroda.ru/documents/'
        res3 = requests.get(url3,headers=headers,cookies=cookies)
        print(res3.status_code)
        print(res3.cookies[str_00])
        ############## 4-й запрос #############
        #print('')
        #print('*********  4  ************')
        headers=parse_file('mu_header4.txt')
        headers['Content-Type'] = 'application/json'
        headers['Origin']='https://pamyat-naroda.ru'
        headers['Referer']='https://pamyat-naroda.ru/documents/'

        bs = res3.cookies[str_00]
        bs += "=" * ((4 - len(res3.cookies[str_00]) % 4) % 4)
        bs = base64.b64decode(bs).decode()
        a_bs = bs.split('XXXXXX')[0]
        b_bs = bs.split('XXXXXX')[1].split('YYYYYY')[0]
        data_t = Template('{"query":{"bool":{"should":[{"bool":{"should":[{"match_phrase":{"document_type":"Боевые донесения, оперсводки"}},{"match_phrase":{"document_type":"Боевые приказы и распоряжения"}},{"match_phrase":{"document_type":"Отчеты о боевых действиях"}},{"match_phrase":{"document_type":"Переговоры"}},{"match_phrase":{"document_type":"Журналы боевых действий"}},{"match_phrase":{"document_type":"Директивы и указания"}},{"match_phrase":{"document_type":"Приказы"}},{"match_phrase":{"document_type":"Постановления"}},{"match_phrase":{"document_type":"Доклады"}},{"match_phrase":{"document_type":"Рапорты"}},{"match_phrase":{"document_type":"Разведывательные бюллетени и донесения"}},{"match_phrase":{"document_type":"Сведения"}},{"match_phrase":{"document_type":"Планы"}},{"match_phrase":{"document_type":"Планы операций"}},{"match_phrase":{"document_type":"Карты"}},{"match_phrase":{"document_type":"Схемы"}},{"match_phrase":{"document_type":"Справки"}},{"match_phrase":{"document_type":"Прочие документы"}}]}},{"bool":{"should":[{"bool":{"must":[{"range":{"date_from":{"lte":"${finish_date}"}}},{"range":{"date_to":{"gte":"${start_date}"}}}],"boost":3}},{"bool":{"must":[{"range":{"document_date_b":{"lte":"${finish_date}"}}},{"range":{"document_date_f":{"gte":"${start_date}"}}}],"boost":7}}]}},{"bool":{"should":[{"match_phrase":{"authors_list.keyword":{"query":"${military_unit}","boost":50}}},{"match":{"document_name":{"query":"${military_unit}","type":"phrase","boost":30}}},{"match":{"authors":{"query":"${military_unit}","type":"phrase","boost":20}}},{"match":{"army_unit_label.division":{"query":"${military_unit}","type":"phrase","boost":10}}},{"nested":{"path":"page_magazine","query":{"bool":{"must":[{"match":{"page_magazine.podrs":{"query":"${military_unit}","type":"phrase"}}},{"range":{"page_magazine.date_from":{"lte":"${finish_date}"}}},{"range":{"page_magazine.date_to":{"gte":"${start_date}"}}}]}},"boost":4}}]}}],"minimum_should_match":3}},"_source":["id","document_type","document_number","document_date_b","document_date_f","document_name","archive","fond","opis","delo","date_from","date_to","authors","geo_names","operation_name","secr","image_path","delo_id","deal_type","operation_name"],"size":10,"from":0}')

        #data_t= Template('{"query":{"bool":{"should":[{"bool":{"should":[{"match_phrase":{"document_type":"Боевые донесения, оперсводки"}},{"match_phrase":{"document_type":"Боевые приказы и распоряжения"}},{"match_phrase":{"document_type":"Отчеты о боевых действиях"}},{"match_phrase":{"document_type":"Переговоры"}},{"match_phrase":{"document_type":"Журналы боевых действий"}},{"match_phrase":{"document_type":"Директивы и указания"}},{"match_phrase":{"document_type":"Приказы"}},{"match_phrase":{"document_type":"Постановления"}},{"match_phrase":{"document_type":"Доклады"}},{"match_phrase":{"document_type":"Рапорты"}},{"match_phrase":{"document_type":"Разведывательные бюллетени и донесения"}},{"match_phrase":{"document_type":"Сведения"}},{"match_phrase":{"document_type":"Планы"}},{"match_phrase":{"document_type":"Планы операций"}},{"match_phrase":{"document_type":"Карты"}},{"match_phrase":{"document_type":"Схемы"}},{"match_phrase":{"document_type":"Справки"}},{"match_phrase":{"document_type":"Прочие документы"}}]}},{"bool":{"should":[{"bool":{"must":[{"range":{"date_from":{"lte":"${finish_date}"}}},{"range":{"date_to":{"gte":"${start_date}"}}}],"boost":3}},{"bool":{"must":[{"range":{"document_date_b":{"lte":"${finish_date}"}}},{"range":{"document_date_f":{"gte":"${start_date}"}}}],"boost":7}}]}}],"minimum_should_match":2}},"_source":["id","document_type","document_number","document_date_b","document_date_f","document_name","archive","fond","opis","delo","date_from","date_to","authors","geo_names","operation_name","secr","image_path","delo_id","deal_type","operation_name"],"size":"${size}","from":"${para_from}"}')  
        
        data_ = data_t.safe_substitute(start_date='1945-5-1',finish_date='1945-5-31', military_unit=military_unit,size=10,para_from=0)
        url4 = 'https://cdn.pamyat-naroda.ru/data/'+a_bs+'/'+b_bs+'/pamyat/document,map,magazine/_search'
        res4 = requests.post(url4,data=data_.encode('utf-8'),headers=headers)
        if(res4.status_code==200):
            data = json.loads(res4.text)
            total = data['hits']['total']
            hits = data['hits']['hits']
            #print(hits[0]['_source'])
            #for key, value in hits[0].items():
            #    print (key, value)
            divisor = 100
            one, two =divmod (total,divisor)
            print(one, two)
            x=0
            f = open("myfile.html", "w")
            f.write('<html><table border="1" cellpadding="3">')
            head = '<td>Тип документа</td><td>Содержание</td><td>Период</td><td>Авторы</td><td>Дата документа</td><td>Архив</td><td>Фонд</td><td>Опись</td><td>Дело</td><td>Скан</td>'
            f.write(head)
            table_string = Template('<tr><td>${col1}</td><td>${col2}</td><td>${col3}</td><td>${col4}</td><td>${col5}</td><td>${col6}</td><td>${col7}</td><td>${col8}</td><td>${col9}</td><td>${col10}</td></tr>')

            while(x< one*divisor):
                print(divisor, x, total)
                data_ = data_t.safe_substitute(start_date='1945-5-1',finish_date='1945-5-31', military_unit=military_unit,size=divisor,para_from=x)
                url4 = 'https://cdn.pamyat-naroda.ru/data/'+a_bs+'/'+b_bs+'/pamyat/document,map,magazine/_search'
                res4 = requests.post(url4,data=data_.encode('utf-8'),headers=headers)
                if(res4.status_code==200):
                    data = json.loads(res4.text)
                    hits = data['hits']['hits']
                    for hit in hits:
                        #print(hit['_source'])
                        src = hit['_source']
                        data_string = table_string.safe_substitute(col1=src['document_type'],col2=src['document_name'],col3=src['date_from']+'-'+src['date_to'],col4=src['authors'],col5=src['document_date_f'],col6=src['archive'],col7=src['fond'],col8=src['opis'],col9=src['delo'],col10='<a href=https://cdn.pamyat-naroda.ru/imageloadfull/'+src['image_path']+'>Скан</a>'   )
                        f.write(data_string)
                x+=divisor
            print(two, x)
            data_ = data_t.safe_substitute(start_date='1945-5-1',finish_date='1945-5-31', military_unit=military_unit,size=two,para_from=x)
            url4 = 'https://cdn.pamyat-naroda.ru/data/'+a_bs+'/'+b_bs+'/pamyat/document,map,magazine/_search'
            res4 = requests.post(url4,data=data_.encode('utf-8'),headers=headers)
            if(res4.status_code==200):
                data = json.loads(res4.text)
                hits = data['hits']['hits']
                for hit in hits:
                    src = hit['_source']
                    data_string = table_string.safe_substitute(col1=src['document_type'],col2=src['document_name'],col3=src['date_from']+'-'+src['date_to'],col4=src['authors'],col5=src['document_date_f'],col6=src['archive'],col7=src['fond'],col8=src['delo'],col9=src['opis'],
                    #col10='<a href=https://cdn.pamyat-naroda.ru/imageloadfull/'+src['image_path']+'>Скан</a>')
                    col10='<input value="scan" onclick="window.open(\'https://cdn.pamyat-naroda.ru/imageloadfull/'+ src['image_path']+'\')" type="button">')
                    f.write(data_string)
            f.write('</table></html>')
            f.close()
exit(0)
#https://pamyat-naroda.ru/documents/view/?id=132241172&backurl=division%5C1256%20%D0%B3%D0%B0%D0%BF::begin_date%5C01.05.1945::end_date%5C31.05.1945::use_main_string%5Ctrue::group%5Call::types%5Copersvodki:rasporyajeniya:otcheti:peregovori:jbd:direktivi:prikazi:posnatovleniya:dokladi:raporti:doneseniya:svedeniya:plani:plani_operaciy:karti:shemi:spravki:drugie&date_from=01.05.1945&date_to=31.05.1945&division=1256%20%D0%B3%D0%B0%D0%BF#
#https://cdn.pamyat-naroda.ru/imageloadfull/Передача_057_КП097Р_С45/236-0002673-2731/00000002.jpg
