<template>
  <v-card>
    <v-card-title>
      <v-file-input
        label="Upload savedrecs.txt"
        accept=".txt"
        show-size
        v-model="value"
      />
      <v-btn @click="upload">
        Upload
      </v-btn>
      <v-btn @click="clickGraph">
        Graph
      </v-btn>
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
      @click:row="clickline"
    />
  </v-card>
</template>

<script>
import Dexie from 'dexie';

export default {
  name: 'DataTable',
  data: () => ({
    headers: [
      {
        text: 'Title',
        align: 'start',
        sortable: false,
        value: 'Title',
      },
      { text: 'Auther', sortable: false, value: 'AU' },
      { text: 'Year', value: 'PY' },
      { text: 'LCS', value: 'LCS' },
      { text: 'GCS', value: 'GCS' },
      { text: 'LCR', value: 'LCR' },
      { text: 'CR', value: 'CR' },
    ],
    articles: [
      {
        Title: 'See this before request or request failure',
        PY: 0,
        LCS: 0,
        GCS: 0,
        LCR: 0,
        CR: 0,
        DOI: '10.0000/abcdef',
        AU: 'Jhon',
      },
      {
        Title: 'test row2',
        PY: 10,
        LCS: 10,
        GCS: 10,
        LCR: 10,
        CR: 10,
        DOI: '10.1010/qwerty',
        AU: 'Harry',
      },
    ],
    search: '',
    value: null,
  }),
  methods: {
    readText(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          resolve(reader.result);
        };
        reader.onerror = () => {
          reject(reader.error);
        };
        reader.readAsText(file, 'UTF-8');
      });
    },
    parseText(txt) {
      // eslint-disable-next-line no-control-regex
      const splitChunkMark = new RegExp('\n(?=PT J)', 'm');
      const chunks = txt.split(splitChunkMark).slice(1);
      const localArticleList = chunks
        .map((each) => {
          // eslint-disable-next-line no-control-regex
          const splitLines = each.split(new RegExp('\n'));
          let TILineNum;
          let SOLineNum;
          let TCLineNum;
          let DILineNum;
          let PYLineNum;
          let AULineNum;
          let CRLineNum;
          let NRLineNum;
          for (let lineNum = 0; lineNum < splitLines.length; lineNum += 1) {
            const line = splitLines[lineNum];
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
          }
          if (
            TILineNum !== undefined
            && SOLineNum !== undefined
            && TCLineNum !== undefined
            && DILineNum !== undefined
            && PYLineNum !== undefined
            && AULineNum !== undefined
            && CRLineNum !== undefined
            && NRLineNum !== undefined
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

            const citeList = CRLines.map((citelineWithCap) => {
              const citeline = citelineWithCap.slice(3);
              const citeTitle = citeline.split(new RegExp(', DOI '))[0];
              let citeDOI = citeline.split(new RegExp(', DOI '))[1];
              if (citeTitle !== undefined && citeDOI !== undefined) {
                if (citeDOI.startsWith('[')) {
                  citeDOI = citeDOI.split(',')[0].slice(1);
                }
                return { citeTitle, citeDOI };
              }
              return null;
            }).filter((cite) => cite !== null);

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
        .filter((article) => article !== null);
      return localArticleList;
    },
    findLocalCite(txt) {
      const localArticleList = this.parseText(txt);

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
    },
    async upload() {
      const txt = await this.readText(this.value);
      const localArticleList = this.findLocalCite(txt);
      this.articles = [];

      await Dexie.delete('article_database');
      const db = new Dexie('article_database');
      db.version(1).stores({
        articles:
          'Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR',
      });
      localArticleList.forEach(async (article) => {
        await db.articles.put(article);
        this.articles.push({
          Title: article.Title,
          PY: article.Year,
          LCS: article.LCS,
          GCS: article.GCS,
          LCR: article.LCR,
          CR: article.CR,
          AU: article.Author,
          DOI: article.DOI,
        });
      });
    },
    clickline(payload) {
      const detailPage = this.$router.resolve({
        name: 'Details',
        params: { doi: payload.DOI },
      });
      window.open(detailPage.href, '_blank');
    },
    clickGraph() {
      const graphPage = this.$router.resolve({ name: 'Graph' });
      window.open(graphPage.href, '_blank');
    },
  },
};
</script>

<style>
</style>
