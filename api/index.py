from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, File
import re


class Article(object):
    def __init__(self, doi, ref_list, tc, ti, py):
        self.doi = doi
        self.ref_list = ref_list
        self.cr = len(ref_list)
        self.gcs = tc
        self.lcs = 0
        self.lcr = 0
        self.lcs_list = []
        self.title = ti
        self.year = py


def core(file):
    local_article_list = []
    chunks = re.split(r'\n(?=PT J)', file.decode('utf-8'), flags=re.MULTILINE)

    for each in chunks[1:]:
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
            if re.match(r'PY ', split_lines[line_num]) != None:
                PY_line_num = line_num

        TI_lines = split_lines[TI_line_num:SO_line_num]
        TI = ' '.join(TI_lines).replace('    ', ' ')[3:]

        TC_line = split_lines[TC_line_num]
        TC = int(TC_line[3:])

        DI_line = split_lines[DI_line_num]
        DI = DI_line[3:]

        PY_line = split_lines[PY_line_num]
        PY = PY_line[3:]

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
        local_article_list.append(Article(DI, ref_list, TC, TI, PY))

    for article_use in local_article_list:
        for article_source in local_article_list:
            for ref in article_use.ref_list:
                if ref["ref_doi"] == article_source.doi:
                    article_use.lcr += 1
                    article_source.lcs += 1
                    article_source.lcs_list.append(ref)
    return local_article_list


article_list = []


app = FastAPI()

# origins = ["http://localhost:8080"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.post("/")
def receive_savedrecs(file: bytes = File(...)):
    article_list = core(file)
    return [{"Title": atc.title, "LCS": atc.lcs, "GCS": atc.gcs, "LCR": atc.lcr, "CR": atc.cr, "PY": atc.year} for atc in article_list]


@app.get("/{doi:path}")
def search_doi(doi: str):
    searched_atc = {}
    for atc in article_list:
        if atc.doi == doi:
            searched_atc = {"Title": atc.title, "DOI": atc.doi, "LCS": atc.lcs,
                            "GCS": atc.gcs, "LCR": atc.lcr, "CR": atc.cr, "LCS List": atc.lcs_list}
            break
    if searched_atc == {}:
        raise HTTPException(status_code=404, detail="DOI Not Found")
    else:
        return searched_atc
