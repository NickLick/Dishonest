# 百度url测试
import requests

url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人&pn=3&rn=10&from_mid=1&&oe=utf-8'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36',
    'Referer': 'https://www.baidu.com/s?wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&rsv_spt=1&rsv_iqid=0xf2ddffc700065fc3&issp=1&f'
               '=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_dl=tb&rsv_enter=1&rsv_sug3=11&rsv_sug1=10&rsv_sug7'
               '=100&rsv_sug2=0&rsv_btype=i&prefixsug=%25E5%25A4%25B1%25E4%25BF%25A1%25E4%25BA%25BA&rsp=5&inputT=2456'
               '&rsv_sug4=3025 '
}

if __name__ == '__main__':
    response = requests.get(url, headers=headers)
    print(response.content.decode())
    # card_num='3203251973****8020'
    # print(card_num[:10]+'****'+card_num[14:])
