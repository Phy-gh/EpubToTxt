def EpubToTxt(file):

    import os
    import zipfile
    import re
    from bs4 import BeautifulSoup

    def PrettifyTxt(text):
        lines = text.split('\n')
        text = ''
        for line in lines:
            if line.split():
                text = text + '    ' + line.strip() + '\n'
        return text

    filename = os.path.basename(file)
    filebasename = os.path.splitext(filename)[0]
    zipfile = zipfile.ZipFile(file)
    namelist = zipfile.namelist()
    opflist = []
    text = ''
    
    for subfile in namelist :
        if subfile.endswith('.opf'):
            opflist.append(subfile)
    opffile = min(opflist,key = len)
    folder = opffile.rstrip(os.path.basename(opffile))
    opfs = zipfile.open(opffile)
    opf = ''
    for line in opfs:
        opf = opf + str(line,'utf-8')
    ncx = re.search('(?s)<spine.*toc.*=.*"ncx".*>(.*?)</spine>',opf,re.M).group()
    manifest = re.search('(?s)<manifest.*>(.*?)</manifest>',opf,re.M).group()

    ids = re.findall(' id="(.*?)"',manifest)
    hrefs = re.findall('href="(.*?)"',manifest)
    idrefs = re.findall('<itemref.*idref="(.*?)"',ncx)
            
    key = dict(zip(ids,hrefs))

    for idref in idrefs:
        htmpath = folder + key[idref]
        htmopen = zipfile.open(htmpath)
        soup = BeautifulSoup(htmopen,'lxml')
        text = text + soup.get_text()

    zipfile.close()
    return PrettifyTxt(text)
