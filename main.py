import re
with open("savedrecs.txt","r") as f:
    chunks = re.split(r'\n(?=PT J)',f.read(),flags=re.MULTILINE)

class Article(object):
    def __init__(self,doi,ref_doi_list,tc):
        self.doi =doi
        self.ref_doi_list = ref_doi_list
        self.cr = len(ref_doi_list)
        self.gcs = tc
        self.lcs = 0
        self.lcr = 0
        self.lcs_doi_list = []

local_article_list = []

for each in chunks[1:]:
    self_doi = re.split(r' ',re.findall(r'DI \d{2}\.\d{4}/.*\n',each)[0])[1]
    self_tc  = int(re.split(r' ',re.findall(r'TC \d*\n',each)[0])[1])
    cr_list = re.findall(r'DOI \[?\d{2}\.\d{4}/.*\n',each)
    ref_doi_list = []
    for cr in cr_list:
        ref_doi_list.append(re.findall(r'\d{2}\.\d{4}/.*?\s',cr)[0].replace(',','\n'))
    local_article_list.append(Article(self_doi,ref_doi_list,self_tc))

for article_use in local_article_list:
    for ref_doi in article_use.ref_doi_list:
        for article_source in local_article_list:
            if ref_doi == article_source.doi:
                article_use.lcr += 1
                article_source.lcs_doi_list.append(ref_doi)
                article_source.lcs += 1

for article in local_article_list:
    if article.lcs != 0:
        print(article.doi ,article.lcs_doi_list)







