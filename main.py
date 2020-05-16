import re
import typer
from tabulate import tabulate
import math

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

app = typer.Typer()



def core(filename):
    local_article_list = []
    with open("{}".format(filename),"r") as f:
        chunks = re.split(r'\n(?=PT J)',f.read(),flags=re.MULTILINE)

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
        TI = ' '.join(TI_lines).replace('    ',' ')[3:]

        TC_line = split_lines[TC_line_num]
        TC = int(TC_line[3:])

        DI_line = split_lines[DI_line_num]
        DI = DI_line[3:]

        CR_lines = split_lines[CR_line_num:NR_line_num]
        ref_list = []
        for line_num in range(len(CR_lines)):
            CR_lines[line_num] = CR_lines[line_num][3:]
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
    return local_article_list


@app.command()
def lcs(filename:str,page:int=typer.Option(0,help="Display articles of next pages")):
    local_article_list = core(filename)
    lcs_sort_list = sorted(local_article_list,key=lambda atc:atc.lcs,reverse=True)
    lcs_show_list = lcs_sort_list[page*20:(page+1)*20]
    lcs_show_table = [(atc.title, atc.doi, atc.lcs,atc.lcr,atc.gcs,atc.cr) for atc in lcs_sort_list]
    header = ["Title","DOI","LCS","LCR","GCS","CR"]
    print(tabulate(lcs_show_table,headers=header))

@app.command()
def lcr(filename:str,page:int=typer.Option(0,help="Display articles of next pages")):
    local_article_list = core(filename)
    lcr_sort_list = sorted(local_article_list,key=lambda atc:atc.lcr,reverse=True)
    lcr_show_list = lcr_sort_list[page*20:(page+1)*20]
    lcr_show_table = [(atc.title, atc.doi, atc.lcs,atc.lcr,atc.gcs,atc.cr) for atc in lcr_sort_list]
    header = ["Title","DOI","LCS","LCR","GCS","CR"]
    print(tabulate(lcr_show_table,headers=header))

@app.command()
def search(filename:str, doi:str):
    local_article_list=core(filename)
    searched_article = next((atc for atc in local_article_list if atc.doi == doi))
    searched_article_table = [[searched_article.title,searched_article.doi,searched_article.lcs,searched_article.lcr,searched_article.gcs,searched_article.cr,searched_article.lcs_list]]
    header = ["Title","DOI","LCS","LCR","GCS","CR","LCS_LIST"]
    print(tabulate(searched_article_table,headers=header))

# @app.command()
# def show():
#     local_article_list=core("savedrecs.txt")
#     for atc in local_article_list:
#         print(atc.title)



    


if __name__ == "__main__":
    app()












