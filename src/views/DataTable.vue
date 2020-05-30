<template>
  <v-card>
    <v-card-title>
      <v-file-input label="Upload savedrecs.txt" accept=".txt" show-size v-model="value" />
      <v-btn @click="upload" color="secondary">Upload</v-btn>
      <v-spacer />
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      />
    </v-card-title>
    <v-data-table
    :headers="headers"
    :items="articles"
    :search="search"
    @click:row="clickline"></v-data-table>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Dexie from 'dexie/dist/dexie';

export function isNotNull<T>(candidate: T|null): candidate is T {
  return candidate !== null;
}

function readText(file: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        resolve(reader.result);
      }
    };
    reader.onerror = () => {
      reject(reader.error);
    };
    reader.readAsText(file, 'UTF-8');
  });
}
interface Cite {
  citeTitle: string;
  citeDOI: string;
}
export interface Article {
  Title: string;
  Journal: string;
  GCS: number;
  DOI: string;
  Year: number;
  Author: string;
  citeList: Cite[];
  LCR: number;
  LCS: number;
  localCiteList: Cite[];
  CR: number;
}


function parseText(txt: string): Article[] {
  // eslint-disable-next-line no-control-regex
  const splitChunkMark = new RegExp('\n(?=PT J)', 'm');
  const chunks = txt.split(splitChunkMark).slice(1);
  const localArticleList: Article[] = chunks
    .map((each) => {
      // eslint-disable-next-line no-control-regex
      const splitLines = each.split(new RegExp('\n'));
      let TILineNum: number|undefined;
      let SOLineNum: number|undefined;
      let TCLineNum: number|undefined;
      let DILineNum: number|undefined;
      let PYLineNum: number|undefined;
      let AULineNum: number|undefined;
      let CRLineNum: number|undefined;
      let NRLineNum: number|undefined;
      splitLines.forEach((line, lineNum) => {
        if (line.startsWith('TI ')) {
          TILineNum = lineNum;
        } else if (line.startsWith('SO ')) {
          SOLineNum = lineNum;
        } else if (line.startsWith('TC ')) {
          TCLineNum = lineNum;
        } else if (line.startsWith('DI ')) {
          DILineNum = lineNum;
        } else if (line.startsWith('PY ')) {
          PYLineNum = lineNum;
        } else if (line.startsWith('AU ')) {
          AULineNum = lineNum;
        } else if (line.startsWith('CR ')) {
          CRLineNum = lineNum;
        } else if (line.startsWith('NR ')) {
          NRLineNum = lineNum;
        }
      });
      if (
        typeof TILineNum !== 'undefined'
        && typeof SOLineNum !== 'undefined'
        && typeof TCLineNum !== 'undefined'
        && typeof DILineNum !== 'undefined'
        && typeof PYLineNum !== 'undefined'
        && typeof AULineNum !== 'undefined'
        && typeof CRLineNum !== 'undefined'
        && typeof NRLineNum !== 'undefined'
      ) {
        const TILines = splitLines.slice(TILineNum, SOLineNum);
        const TI = TILines.join(' ')
          .replace(new RegExp(' {4}', 'g'), ' ')
          .slice(3);

        const SOLine = splitLines[SOLineNum];
        const SO = SOLine.slice(3);

        const TCLine = splitLines[TCLineNum];
        const TC = parseInt(TCLine.slice(3), 10);

        const DILine = splitLines[DILineNum];
        const DI = DILine.slice(3);

        const PYLine = splitLines[PYLineNum];
        const PY = parseInt(PYLine.slice(3), 10);

        const AULine = splitLines[AULineNum];
        const AU = AULine.slice(3);

        const CRLines = splitLines.slice(CRLineNum, NRLineNum);

        const citeList: Cite[] = CRLines.map((citelineWithCap: string): Cite|null => {
          const citeLine = citelineWithCap.slice(3);
          const citeTitle = citeLine.split(new RegExp(', DOI '))[0];
          let citeDOI = citeLine.split(new RegExp(' DOI '))[1];
          if (citeTitle !== undefined && citeDOI !== undefined) {
            if (citeDOI.startsWith('[')) {
              citeDOI = citeDOI.split(',')[0].slice(1);
            }
            return { citeTitle, citeDOI };
          }
          return null;
        }).filter(isNotNull);
        return {
          Title: TI,
          Journal: SO,
          GCS: TC,
          DOI: DI,
          Year: PY,
          Author: AU,
          citeList,
          LCR: 0,
          LCS: 0,
          localCiteList: [],
          CR: citeList.length,
        };
      }
      return null;
    })
    .filter(isNotNull);
  return localArticleList;
}

function findLocalCite(rawArticles: Article[]): Article[] {
  const localArticleList = rawArticles;
  /* eslint no-param-reassign: ["error",
      { "props": true,
        "ignorePropertyModificationsFor": ["articleSource","cite","articleUse"]
      }] */
  localArticleList.forEach((articleUse) => {
    articleUse.citeList.forEach((cite) => {
      localArticleList.forEach((articleSource) => {
        if (cite.citeDOI === articleSource.DOI) {
          articleUse.LCR += 1;
          articleUse.localCiteList.push(cite);
          articleSource.LCS += 1;
        }
      });
    });
  });
  return localArticleList;
}

@Component
export default class DataTable extends Vue {
  search = '';

  headers = [
    {
      text: 'Title',
      align: 'start',
      sortable: false,
      value: 'Title',
    },
    { text: 'Auther', sortable: false, value: 'Author' },
    { text: 'Year', value: 'Year' },
    { text: 'LCS', value: 'LCS' },
    { text: 'GCS', value: 'GCS' },
    { text: 'LCR', value: 'LCR' },
    { text: 'CR', value: 'CR' },
  ];

  articles: Article[] = [
    {
      Title: 'See this before request or request failure',
      Year: 0,
      LCS: 0,
      GCS: 0,
      LCR: 0,
      CR: 0,
      DOI: '10.0000/abcdef',
      Author: 'Jhon',
      Journal: 'Nature',
      citeList: [],
      localCiteList: [],
    },
    {
      Title: 'test row2',
      Year: 10,
      LCS: 10,
      GCS: 10,
      LCR: 10,
      CR: 10,
      DOI: '10.1010/qwerty',
      Author: 'Harry',
      Journal: 'Science',
      citeList: [],
      localCiteList: [],
    },
  ];

  value: Blob|null = null;

  private async upload(): Promise<void> {
    if (this.value !== null) {
      const txt = await readText(this.value);
      const rawArticles = parseText(txt);
      const localArticleList = findLocalCite(rawArticles);
      this.articles = localArticleList;

      await Dexie.delete('article_database');
      const db = new Dexie('article_database');
      db.version(1).stores({
        articles:
        'Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR',
      });
      localArticleList.forEach(async (article) => {
        const articles = db.table('articles');
        await articles.put(article);
      });
    }
  }

  private clickline(payload: any): void {
    const detailPage = this.$router.resolve({
      name: 'Details',
      params: { doi: payload.DOI },
    });
    window.open(detailPage.href, '_blank');
  }
}

</script>

<style>
</style>
