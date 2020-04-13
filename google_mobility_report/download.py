#!/usr/bin/env python3


import os
import datetime

import requests_html


def download_data():
    "Download pdf data and returns raw bytes"

    sess = requests_html.HTMLSession()

    url = 'https://www.google.com/covid19/mobility/'
    resp1 = sess.get(url)

    h1 = resp1.html.find('h1', containing='Brazil')
    if len(h1) != 1:
        msg = (
            f'Excepcted just one h1 tag with "Brazil" string. '
            f'But found {len(h1)}'
        )
        raise ValueError(msg)
    h1 = h1[0]
    parent = h1.element.getparent().getparent()
    link = parent.xpath('.//a')
    if len(link) != 1:
        msg = (
            f'Expected just one "a" tag for Brazil data. '
            f'But found {len(link)}'
        )
        raise ValueError(msg)

    link = link[0].attrib['href']
    date = link.split('/')[-1].split('_')[0]
    date = datetime.datetime.fromisoformat(date)

    resp2 = sess.get(link)
    return resp2.content, date


def make_filename(date):
    dt_str = date.date().isoformat()
    filename = f'{dt_str}_BR_Mobility_Report_en.pdf'
    return filename


def save(content, filename):
    folder_script = os.path.split(os.path.realpath(__file__))[0]
    folder_data = os.path.join(folder_script, 'data')
    fullfilename = os.path.join(folder_data, filename)
    with open(fullfilename, 'wb') as f:
        f.write(content)


if __name__ == '__main__':
    content, date = download_data()
    filename = make_filename(date)
    save(content, filename)
    
