def EpubToTxt(file):

    import os
    import zipfile
    import re
    import html2text
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
    path = file.strip('/'+filename)
    savepath = path + filebasename
    zipfile = zipfile.ZipFile(file)
    namelist = zipfile.namelist()
    subfilelist = []
    flag = {}
    text = ''

    for subfile in namelist :
        flag1 = subfile.endswith('.html')
        flag2 = subfile.endswith('.htm')
        flag3 = subfile.endswith('.xhtml')
        if flag1 or flag2 or flag3 :
            flag[subfile] = True

    for subfile in namelist :
        if subfile.endswith('.opf'):
            folder = subfile.rstrip(os.path.basename(subfile))
            opfs = zipfile.open(subfile)
            opf = ''
            for line in opfs:
                opf = opf + str(line,'utf-8')
            left1 = re.search('<spine toc="ncx">',opf).span()[0]
            left2 = re.search('<manifest>',opf).span()[0]
            right1 = re.search('</spine>',opf).span()[1]
            right2 = re.search('</manifest>',opf).span()[1]
            ncx = opf[left1:right1]
            manifest = opf[left2:right2]
            
            ids = re.findall('id="(.*?)"',manifest)
            hrefs = re.findall('href="(.*?)"',manifest)
            idrefs = re.findall('<itemref idref="(.*?)"',ncx)
            
            key = {}
            

            for i in range(0,len(ids)):
                    key[ids[i]] = hrefs[i]

            for idref in idrefs:
                htmpath = folder + key[idref]
                if htmpath in flag.keys() and flag[htmpath] :
                    htmopen = zipfile.open(htmpath)
                    soup = BeautifulSoup(htmopen,'lxml')
                    text = text + soup.get_text()
                    flag[htmpath] = False
                else :
                    pass

    zipfile.close()

    return PrettifyTxt(text)
