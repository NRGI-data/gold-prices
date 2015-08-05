import os
import urllib
import logging
import csv
import shutil

source_url = 'http://www.bundesbank.de/cae/servlet/StatisticDownload?tsId=BBEX3.M.XAU.USD.EA.AC.C06&its_csvFormat=en&its_fileFormat=csv&mode=its'

def download():
    if not os.path.exists(args.filepath + '/cache'):
        os.makedirs(args.filepath + '/cache')
    urllib.urlretrieve(source_url, downloaded)

def extract():
    reader = csv.reader(open(downloaded))
    newrows = [ row for row in reader ]
    # skip top 5 rows
    newrows = newrows[5:]
    # trim the notes from the bottom
    newrows = newrows[:-1]
    # fix up the data
    # dates are 1968-06 without day ...
    newrows = [ [row[0] + '-01', row[1]] for row in newrows ]

    existing = []
    if os.path.exists(outpath):
        fo = open(outpath)
        existing = [ row for row in csv.reader(fo) ]
        fo.close()
    
    starter = newrows[0]
    for idx,row in enumerate(existing):
        if row[0] == starter[0]:
            # remove all rows from here on
            del existing[idx:]
            break
    # and now add in new data
    outrows = existing + newrows
    fo = open(outpath, 'w')
    writer = csv.writer(fo)
    writer.writerows(outrows)
    fo.close()
    shutil.rmtree(args.filepath + '/cache')

# import os
# os.environ['http_proxy'] = ''
# def upload():
#     import datastore.client as c
#     dsurl = 'http://datahub.io/dataset/gold-prices/resource/b9aae52b-b082-4159-b46f-7bb9c158d013'
#     client = c.DataStoreClient(dsurl)
#     client.delete()
#     client.upload(outpath)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    import argparse
    parser = argparse.ArgumentParser(
        description='download and update bundesbank list of monthly gold spot prices')

     # Output file option
    parser.add_argument('-o', '--output', dest='filepath', action='store',
                        default=None, metavar='filepath',
                        help='define output filepath')
    # # Source file (default is the global cpi_source)
    # parser.add_argument('source', default=cpi_source, nargs='?',
    #                     help='source file to generate output from')
    # Parse the arguments into args
    args = parser.parse_args()

    downloaded = args.filepath + '/cache/bbk_WU5500.csv'
    outpath = args.filepath + '/data/data.csv'  

    print 'Downloading'
    download()
    print 'Extracting and merging'
    extract()
    
