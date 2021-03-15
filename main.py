

'''Main module'''
import json

from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
from tqdm import tqdm

import xml_writer
from args import args
from constants import MONTHS
from constants import URL


def get_raw_data(year):
    session = FuturesSession()
    futures = [{
        'month': m,
        'future': session.get(URL.format(year=year, month=m), timeout=30),
    } for m in MONTHS]
    pbar = tqdm(total=len(futures))
    data = []
    for future in futures:
        response = future['future'].result()
        data.append({'month': future['month'], 'data': response.content.decode('utf-8')})
        pbar.update()

    return data


def main():
    '''Main function'''
    if args.data is None:
        data = get_raw_data(args.year)
    else:
        with open(args.data) as fp:
            data = json.load(fp)
    dashi_l = {}
    nday_l = {}
    eday_l = {}
    fest_l = {}
    holiday_l = {}

    for month_data in data:
        month = month_data['month']
        dashi_l[month] = []
        nday_l[month] = []
        eday_l[month] = []
        fest_l[month] = []
        holiday_l[month] = []

        soup = BeautifulSoup(month_data['data'], 'html.parser')
        dashi = soup.findAll('div', {'id': 'dashi'})
        nday = soup.findAll('div', {'id': 'nday'})
        eday = soup.findAll('div', {'id': 'eday'})
        fest = soup.findAll('div', {'id': 'fest'})

        for w in range(0, 5):
            for i in range(1, 5):
                for j in range(0, 7):
                    if i == 1:
                        if (dashi[j+w*7].font != None):
                            dashi_l[month].append(dashi[j+w*7].font.string)
                        else:
                            dashi_l[month].append(' ')

                    if i == 2:
                        if (nday[j+w*7].font.string != None):
                            nday_l[month].append(nday[j+w*7].font.string)
                            if nday[j+w*7].font['color'] == 'red':
                                holiday_l[month].append('holiday')
                            else:
                                holiday_l[month].append('normal')

                        else:
                            nday_l[month].append(' ')
                            holiday_l[month].append('normal')

                    if i == 3:
                        if (eday[j+w*7].font.string != None):
                            eday_l[month].append(eday[j+w*7].font.string)
                        else:
                            eday_l[month].append(' ')

                    if i == 4:
                        if (fest[j+w*7].font != None):
                            if(fest[j+w*7].font.string != None):
                                fest_l[month].append(fest[j+w*7].font.string)
                            else:
                                fest_l[month].append(' ')
                                continue
                        else:
                            fest_l[month].append(' ')

    xml_writer.write(dashi_l, eday_l, nday_l, fest_l, holiday_l)


if __name__ == '__main__':
    main()
