# user config
# -------------------------------------------------------
returnXLS = True # write result into a xls document
returnConfig = True # write mission information into a txt document
silenceMode = False # whether the program will have output
isCommandShell = False # command shell mode: catchMovie.py [movie name] or just input
timeWait = 1 # Time wait for every page catch (short time wait may cause unsucceed catch)
# -------------------------------------------------------
# user config end

from lxml import etree
import requests as rq
import time
import xlwt
import os
import sys

# get the web content three (adapt the the xpath form)
def getUrlTree(page,content):
    page = str(page)
    url = 'http://ifkdy.com/index.php?p=' + page + '&q=' +  content
    return etree.HTML(rq.get(url, timeout=5).content)

# write the result
def write_excel():
    def set_style(name, height, bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('Movie',cell_overwrite_ok=True)
    row0 = ["Description","Resource","URL"]
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
    for i in range(0,len(desc)):
        sheet1.write(i+1, 0, desc[i],set_style('Times New Roman',220,True))
        sheet1.write(i+1, 1, res[i], set_style('Times New Roman',220,True))
        sheet1.write(i+1, 2, addr[i], set_style('Times New Roman', 220, True))
    f.save('movie.xls')

# write the mission config
def write_Config():
    f = open('movie.txt','w')
    f.write(missionInfo)

# MAIN PROGRAM
# initialize
page = 1
total = 0
PerPageMovie = 20
resource = []

# remove the old document
try:
    os.remove('movie.xls')
    os.remove('movie.txt')
except BaseException:
    print()

# ask for movie name
if not isCommandShell:
    movie = str(input('Please input the movie you want to watch: '))
else:
    data = sys.argv
    if len(data) != 2:
        print('you must and only can have 1 parameter: catchMovie.py [movie name]')
        os._exit(0)
    movie = data[1]

# Resource Info
TotalMovie = int(getUrlTree(1000,'2001').xpath('/html/body/div[2]/p/span[1]/text()')[0][4:][:-1])
NeededPage = int(TotalMovie/PerPageMovie)

while True:
    if page == NeededPage:
        break
    pageResource = getUrlTree(page,movie) # resource for this page
    for movieCount in range(PerPageMovie):
        try:
            xpAddr = '/html/body/div[2]/div[1]/ul/li[' + str(movieCount) + ']/a/span[1]/text()'
            xpDesc = '/html/body/div[2]/div[1]/ul/li[' + str(movieCount) + ']/a/span[2]/text()'
            xpUrl = '/html/body/div[2]/div[1]/ul/li[' + str(movieCount) + ']/a/@href'
            # analyze the information
            info = {}
            info[pageResource.xpath(xpDesc)[0]] = (pageResource.xpath(xpAddr)[0],pageResource.xpath(xpUrl)[0])
            resource.append(info)
            total += 1
            if not silenceMode:
                print(info)
        except BaseException:
            continue
    time.sleep(timeWait)
    page += 1 # another page

# return mission config
missionInfo = ('\n'
      '------------------------\n'
      'Movie Name: ' + movie + '\n' +
      'Total Movie: ' + str(TotalMovie) + '\n'+
      'Succeed Catch:  ' + str(total) + '\n' +
      'Failed Catch: ' + str(TotalMovie - total) +
      '\n------------------------')
if not silenceMode:
    print(missionInfo)

# rewrite description into list
desc = list(map(lambda x:list(x.keys())[0],resource))
addr = list(map(lambda x:list(x.values())[0][1],resource))
res = list(map(lambda x:list(x.values())[0][0],resource))

try:
    if returnXLS:
        write_excel()
    if returnConfig:
        write_Config()
except BaseException:
    print('write fail')