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
import {
  Article, parseText, findLocalCite,
} from '../logic/textToArticles';


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
      Abstract: 'Abstract1',
      AuthorsList: [],
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
      Abstract: 'Abstract2',
      AuthorsList: [],
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
        'Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR,Abstract,AuthorsList',
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
