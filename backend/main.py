from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, File
import re


class Article(object):
    def __init__(self, doi, ref_list, tc, ti, py, au, so):
        self.doi = doi
        self.ref_list = ref_list
        self.cr = len(ref_list)
        self.gcs = tc
        self.lcs = 0
        self.lcr = 0
        self.lcs_list = []
        self.title = ti
        self.year = py
        self.author = au
        self.journal = so


def core(file):
    local_article_list = []
    chunks = re.split(r'\n(?=PT J)', file.decode('utf-8'), flags=re.MULTILINE)

    for each in chunks[1:]:
        try:
            split_lines = each.splitlines()
            for line_num in range(len(split_lines)):
                if re.match(r'TI ', split_lines[line_num]) != None:
                    TI_line_num = line_num
                if re.match(r'SO ', split_lines[line_num]) != None:
                    SO_line_num = line_num
                if re.match(r'CR ', split_lines[line_num]) != None:
                    CR_line_num = line_num
                if re.match(r'NR ', split_lines[line_num]) != None:
                    NR_line_num = line_num
                if re.match(r'TC ', split_lines[line_num]) != None:
                    TC_line_num = line_num
                if re.match(r'DI ', split_lines[line_num]) != None:
                    DI_line_num = line_num
                if re.match(r'PY \d{4}', split_lines[line_num]) != None:
                    PY_line_num = line_num
                if re.match(r'AU ', split_lines[line_num]) != None:
                    AU_line_num = line_num

            TI_lines = split_lines[TI_line_num:SO_line_num]
            TI = ' '.join(TI_lines).replace('    ', ' ')[3:]

            SO_line = split_lines[SO_line_num]
            SO = SO_line[3:]

            TC_line = split_lines[TC_line_num]
            TC = int(TC_line[3:])
            try:
                DI_line = split_lines[DI_line_num]
                DI = DI_line[3:]
            except IndexError:
                pass

            try:
                PY_line = split_lines[PY_line_num]
                PY = PY_line[3:]
            except IndexError:
                pass

            AU_line = split_lines[AU_line_num]
            AU = AU_line[3:]

            CR_lines = split_lines[CR_line_num:NR_line_num]
            ref_list = []
            for line_num in range(len(CR_lines)):
                CR_lines[line_num] = CR_lines[line_num][3:]
                if len(CR_lines[line_num].split(', DOI ')) != 2:
                    continue
                ref_title, doi = CR_lines[line_num].split(
                    ', DOI ')[0], CR_lines[line_num].split(', DOI ')[1]
                if doi[0] == '[':
                    doi = doi.split(',')[0].lstrip('[')
                ref = {"ref_title": ref_title, "ref_doi": doi}
                ref_list.append(ref)
            local_article_list.append(
                Article(DI, ref_list, TC, TI, PY, AU, SO))
        except:
            print(each)
            print("-----------")

    for article_use in local_article_list:
        for article_source in local_article_list:
            for ref in article_use.ref_list:
                if ref["ref_doi"] == article_source.doi:
                    article_use.lcr += 1
                    article_source.lcs += 1
                    article_source.lcs_list.append(article_use.doi)
    return local_article_list


class PostArticles (object):
    def __init__(self):
        self.article_list = []

    def set(self, article_list):
        self.article_list = article_list

    def get(self):
        return self.article_list


postcache = PostArticles()


app = FastAPI()
origins = ["http://localhost:8080", "https://citenet.lxj230.xyz"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
def receive_savedrecs(file: bytes = File(...)):
    article_list = core(file)
    postcache.set(article_list)
    return [{"Title": atc.title, "LCS": atc.lcs, "GCS": atc.gcs, "LCR": atc.lcr, "CR": atc.cr, "PY": atc.year, "AU": atc.author, "DOI": atc.doi} for atc in article_list]


@app.get("/doi/{doi:path}")
def search_doi(doi: str):
    article_list = postcache.get()
    searched_atc = {}
    for atc in article_list:
        if atc.doi == doi:
            searched_atc = {"Title": atc.title,
                            "DOI": atc.doi, "Author": atc.author, "Year": atc.year, "Journal": atc.journal}
            break
    if searched_atc == {}:
        raise HTTPException(status_code=404, detail="DOI Not Found")
    else:
        return searched_atc


@app.get("/graph")
def draw_graph(nodes: int = 20):
    article_list = sorted(
        postcache.get(), key=lambda atc: atc.lcs+atc.lcr, reverse=True)[:nodes]
    article_list.sort(key=lambda atc: atc.lcs)
    node_list = [{"id": atc.doi, "label": atc.author} for atc in article_list]
    edge_list = []
    for atc_source in article_list:
        for atc_use in article_list:
            if atc_use.doi in atc_source.lcs_list:
                edge_list.append(
                    {"source": atc_use.doi, "target": atc_source.doi})
    return{"node_list": node_list, "edge_list": edge_list}
