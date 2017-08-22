#!/usr/bin/python
# scrape_tipidpc.py - This script will get all the details needed for a particular
# computer parts.

import requests
from bs4 import BeautifulSoup

filename_ifs = 'tipidpc_ifs.csv'  # File name for tipidpc's new items for sale list
filename_wtb = 'tipidpc_wtb.csv'  # File name for tipidpc's new want to buys list
headers = 'item,price,category,location\n'

f_ifs = open(filename_ifs, 'w')
f_ifs.write(headers)

f_wtb = open(filename_wtb, 'w')
f_wtb.write(headers)

filenames = [f_ifs, f_wtb]

response = requests.get('https://tipidpc.com')
response.raise_for_status

print 'Downloading...'
soup = BeautifulSoup(response.content, 'html.parser')
print 'Done.'
print

main_container = soup.find('div', {'id': 'main'})
windows = main_container.findAll('div', {'class': 'window'})

for i in range(len(windows)):
    title = windows[i].find('h3').text
    print title

    for product in windows[i].findAll('li'):
        item = product.findAll('a')[0].text
        price = product.find('strong').text
        category = product.findAll('a')[1].text
        location = product.find('span').text

        print '\titem:', item
        print '\tprince:', price
        print '\tcategory:', category
        print '\tlocation:', location.strip('()')
        print

        filenames[i].write('"%s"' % item + ',' +
                           price + ',' +
                           category + ',' +
                           '"%s"' % location.strip('()') + '\n')

    print

f_ifs.close()
f_wtb.close()
