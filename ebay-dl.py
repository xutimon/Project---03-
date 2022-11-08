import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv
def parse_itemssold(text): 
    numbers=''
    for char in text:
        if char in '1234567890':
            numbers+=char 
    if 'sold' in text:
        return int(numbers)
    else:
        return 0
def parse_itemprice(text):
    numbers=''
    if text[0]=='$':
        for char in text:
            if char in '1234567890':
                numbers+=char
            elif char=='':
                break
        return int(numbers)
    else:
        return None
def parse_itemshipping(text):
    numbers=''
    if text[0]=='+':
        for char in text:
            if char in '1234567890':
                numbers+=char 
            elif char=='':
                break
        return int(numbers)
    else:
        return 0  

parser=argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
parser.add_argument('search_term')
parser.add_argument('--num_pages', default=10)
parser.add_argument('--csv', action='store_true')
args=parser.parse_args()
print('args.search_term=', args.search_term)
items=[]



for page_number in range(1,int(args.num_pages)+1):
    url='https://www.ebay.com/sch/i.html?_from=R40&_nkw='
    url+=args.search_term 
    url+='&_sacat=0&rt=nc&_pgn='
    url+= str(page_number)
    print('url=', url)



    r= requests.get(url)
    status=r.status_code
    print('status=', status)
    html=r.text
    soup=BeautifulSoup(html,"html.parser")
    
    tags_items=soup.select('.s-item')
    for tag_item in tags_items:
        
        name=None
        tags_name=tag_item.select('.s-item__title')
        for tag in tags_name:
            name=tag.text
    
        freereturns= False
        tags_freereturns=tag_item.select('.s-item__free-returns')   
        for tag in tags_freereturns:
            freereturns=True

        items_sold=None
        tags_itemssold=tag_item.select('.s-item__hotness')
        for tag in tags_itemssold:
            items_sold=parse_itemssold(tag.text)

        price= None 
        tags_itemprice=tag_item.select('.s-item__price')
        for tag in tags_itemprice:
            price=parse_itemprice(tag.text)
        
        shipping= None 
        tags_itemshipping=tag_item.select('.s-item__shipping, .s-item__logisticscost, .s-item__freeXDays')
        for tag in tags_itemshipping:
            shipping=parse_itemshipping(tag.text)

        status= None
        tags_itemstatus=tag_item.select('.SECONDARY_INFO')
        for tag in tags_itemstatus:
            status=tag.text
        
        item={
            'name': name,
            'free_returns': freereturns,
            'items_sold':items_sold,
            'price':price,
            'shipping':shipping,
            'status':status
        }
        items.append(item)


    
    print('len(tags_items)=',len(tags_items))
    print('len(items)=', len(items)) 
     


    if args.csv:
        filename=args.search_term+'.csv'
        with open(filename, 'w') as x:
            header=items[0].keys()
            writer = csv.DictWriter(x, fieldnames=header)
            writer.writeheader()
            writer.writerows(items[1:])
    else:
        filename=args.search_term+'.json'
        with open(filename, 'w', encoding='ascii') as f:
            f.write(json.dumps(items[1:]))
          

