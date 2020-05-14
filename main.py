import re
with open("savedrecs.txt","r") as f:
    chunks = re.split(r'\n(?=PT J)',f.read(),flags=re.MULTILINE)

class Article(object):
    def __init__(self,doi,ref_list,tc,ti):
        self.doi =doi
        self.ref_list = ref_list
        self.cr = len(ref_list)
        self.gcs = tc
        self.lcs = 0
        self.lcr = 0
        self.lcs_list = []
        self.title = ti

local_article_list = []

for each in chunks[1:]:
    split_lines = each.splitlines()
    for line_num in range(len(split_lines)):
        if re.match(r'TI ',split_lines[line_num]) != None:
            TI_line_num = line_num
        if re.match(r'SO ',split_lines[line_num]) != None:
            SO_line_num = line_num
        if re.match(r'CR ',split_lines[line_num]) != None:
            CR_line_num = line_num
        if re.match(r'NR ',split_lines[line_num]) != None:
            NR_line_num = line_num
        if re.match(r'TC ',split_lines[line_num]) != None:
            TC_line_num = line_num
        if re.match(r'DI ',split_lines[line_num]) != None:
            DI_line_num = line_num

    TI_lines = split_lines[TI_line_num:SO_line_num]
    TI = ' '.join(TI_lines).replace('    ',' ').lstrip('TI ')

    TC_line = split_lines[TC_line_num]
    TC = int(TC_line.lstrip('TC '))

    DI_line = split_lines[DI_line_num]
    DI = DI_line.lstrip('DI ')

    CR_lines = split_lines[CR_line_num:NR_line_num]
    ref_list = []
    for line_num in range(len(CR_lines)):
        if line_num == 0:
            CR_lines[line_num] = CR_lines[line_num].lstrip('CR ')
        else:
            CR_lines[line_num] = CR_lines[line_num].lstrip(' ')
        if len(CR_lines[line_num].split(', DOI ')) != 2:
            continue
        ref_title, doi = CR_lines[line_num].split(', DOI ')[0],CR_lines[line_num].split(', DOI ')[1]
        if doi[0] == '[':
            doi = doi.split(',')[0].lstrip('[')
        ref = {"ref_title":ref_title,"ref_doi":doi}
        ref_list.append(ref)   
    local_article_list.append(Article(DI,ref_list,TC,TI))

for article_use in local_article_list:
    for article_source in local_article_list:
        for ref in article_use.ref_list:
            if ref["ref_doi"] == article_source.doi:
                article_use.lcr += 1
                article_source.lcs += 1
                article_source.lcs_list.append(ref)

for article in local_article_list:
    print(article.lcs_list)













