<template>
  <v-container fluid>
    <v-row align="center">
      <v-col>
        <v-file-input
          label="Upload savedrecs.txt"
          accept=".txt"
          show-size
          v-model="ArrayOfFile"
        />
      </v-col>
      <v-col>
        <v-btn color="secondary" @click="clickUpload">Upload</v-btn>
      </v-col>
      <!-- <v-spacer /> -->
      <v-col
        ><v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-data-table
          :headers="headers"
          :items="articles"
          :search="search"
          @click:row="clickLine"
        ></v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>
<script lang="ts" setup>
import { ref,Ref } from 'vue';
import { parseText, findLocalCite, Article } from '../utils/textToArticles';
import Dexie from 'dexie';
import { useRouter } from 'vue-router';
const router = useRouter();
function clickLine(event:Event, value:any) {
  const DOI = value.item.value.DOI;
  const DOIBase64 = btoa(DOI);
  const detailPage = router.resolve({
    name: 'Details',
    params: { doi: DOIBase64 },
  });
  window.open(detailPage.href, '_blank');
  // console.log();
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
const ArrayOfFile = ref([]);
const articles:Ref<Article[]> = ref([
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
]);
async function clickUpload() {
  const file = ArrayOfFile.value[0];
  if (file == undefined) {
    throw new Error('File undefined!!!');
  }
  const txt = await readText(file);
  const rawArticles = parseText(txt);
  const localArticleList = findLocalCite(rawArticles);
  articles.value = localArticleList;
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
  // console.log(localArticleList);
}
const search = ref('');
const headers: Ref<{title:string; key:string; algin?:string|undefined; sortable?:boolean|undefined}[]> = ref([
  {
    title: 'Title',
    align: 'start',
    sortable: false,
    key: 'Title',
  },
  { title: 'Auther', sortable: false, key: 'Author' },
  { title: 'Year', key: 'Year' },
  { title: 'Journal', key: 'Journal'},
  { title: 'LCS', key: 'LCS' },
  { title: 'GCS', key: 'GCS' },
  { title: 'LCR', key: 'LCR' },
  { title: 'CR', key: 'CR' },
]);
</script>
