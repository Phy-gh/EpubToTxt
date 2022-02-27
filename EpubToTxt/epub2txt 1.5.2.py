import os, zipfile, re
from bs4 import BeautifulSoup

def PrettifyTxt(text):
    lines = text.split('\n')
    text = ''
    for line in lines:
        if line.split():
            text = text + line.rstrip() + '\n'
    return text

def epub2txt(epub_file):
    zip_file = zipfile.ZipFile(epub_file)
    namelist = zip_file.namelist()
            
    opffile = sorted(namelist,key=lambda x: (not x.endswith('.opf'),len(x)))[0]
    folder = opffile.rstrip(os.path.basename(opffile))

    with zip_file.open(opffile) as fo:
        opf = str(fo.read(),'utf-8')
        
    ncx = re.search('(?s)<spine.*toc.*=.*"ncx".*>(.*?)</spine>',
                    opf,re.M).group()
    manifest = re.search('(?s)<manifest.*>(.*?)</manifest>',
                         opf,re.M).group()

    ids = re.findall(' id="(.*?)"',manifest)
    hrefs = re.findall('href="(.*?)"',manifest)
    idrefs = re.findall('<itemref.*idref="(.*?)"',ncx)
            
    key = dict(zip(ids,hrefs))

    text = ''.join([BeautifulSoup(zip_file.open
                   (os.path.join(folder,key[idref])),'lxml').get_text()
                  for idref in idrefs])

    zip_file.close()
    
    return PrettifyTxt(text)
