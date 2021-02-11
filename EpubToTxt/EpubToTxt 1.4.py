def EpubToTxt(file):
    
    import os
    import shutil
    import zipfile
    from bs4 import BeautifulSoup
    import re

    def GetTxt(htm):
        with open(htm,encoding='utf-8') as htmopen:
            soup = BeautifulSoup(htmopen,'lxml')
            text = soup.get_text()
            htmopen.close()
        return text

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
    savepath = path + '/' + filebasename
    fileopen = zipfile.ZipFile(file)
    namelist = fileopen.namelist()
    subfilelist = []
    text = ''
    
    for subfile in namelist :
        splitfile = os.path.splitext(subfile)
        flag1 = splitfile[1] == '.html'
        flag2 = splitfile[1] == '.htm'
        flag3 = splitfile[1] == '.xhtml'
        filepath = savepath + '/' + subfile
        if flag1 or flag2 or flag3 :
            try :
                fileopen.extract(subfile,savepath)
            except zipfile.BadZipFile :
                print (filename + ' Is Corrupted!!!')
                shutil.rmtree (savepath)
                return None
                break
            subfilelist.append(subfile)

    for subfile in namelist :
        splitfile = os.path.splitext(subfile)
        flag4 = splitfile[1] == '.opf'
        filepath = savepath + '/' + subfile
        if flag4 :
            opfpath = savepath + '/' + subfile
            try :
                fileopen.extract(subfile,savepath)
            except zipfile.BadZipFile :
                print (filename + ' Is Corrupted!!!')
                shutil.rmtree (savepath)
                return None
                break
            
            with open (opfpath,encoding='utf-8') as opf_open:
                opf = opf_open.read()
                left1 = re.search('<spine toc="ncx">',opf).span()[0]
                left2 = re.search('<manifest>',opf).span()[0]
                right1 = re.search('</spine>',opf).span()[1]
                right2 = re.search('</manifest>',opf).span()[1]
                ncx = opf[left1:right1]
                manifest = opf[left2:right2]
                opfpath = opfpath.strip('/'+os.path.basename(subfile))
                htms = re.findall('<itemref idref="(.*?)"',ncx)
                ids = re.findall('id="(.*?)"',manifest)
                hrefs = re.findall('href="(.*?)"',manifest)
                key = {}
                
                for i in range(0,len(ids)):
                    key[ids[i]] = hrefs[i]
                for htm in htms:
                    htmpath = opfpath + '/' + key[htm]
                    try:
                        text = text + GetTxt(htmpath)
                    except FileNotFoundError:
                        pass
                    else:
                        os.remove(htmpath)
            
    fileopen.close()
    
    shutil.rmtree (savepath)
                
    text = PrettifyTxt(text)
    
    return text
