<template>
  <v-table>
    <tbody>
      <tr>
        <td>Title</td>
        <td>{{ article.Title }}</td>
      </tr>
      <tr>
        <td>Author</td>
        <td>{{ article.AuthorsList[0] }}</td>
      </tr>
      <tr>
        <td>Corrosponding Author</td>
        <td>{{ corrospondingAuthor }}</td>
      </tr>
      <tr>
        <td>Year</td>
        <td>{{ article.Year }}</td>
      </tr>
      <tr>
        <td>Journal</td>
        <td>{{ article.Journal }}</td>
      </tr>
      <tr>
        <td>LCS</td>
        <td>{{ article.LCS }}</td>
      </tr>
      <tr>
        <td>LCR</td>
        <td>{{ article.LCR }}</td>
      </tr>
      <tr>
        <td>DOI</td>
        <td>
          <a :href="doiURL">{{ article.DOI }}</a>
        </td>
      </tr>
      <tr>
        <td>Abstract</td>
        <td>
          {{ article.Abstract }}
        </td>
      </tr>
    </tbody>
  </v-table>
</template>
<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Dexie from 'dexie';
import last from 'lodash/last';
const article = ref({
  Title: 'Title1',
  Author: 'Who1',
  DOI: '10.0000/abcdef',
  Year: 1900,
  Journal: 'Nature',
  GCS: 10000,
  LCS: 1000,
  LCR: 100,
  CR: 200,
  citeList: [],
  localCiteList: [],
  Abstract: 'Abstract1',
  AuthorsList: [],
});

onMounted(async () => {
  const route = useRoute();
  const DOI = atob(route.params.doi as string);
  const db = new Dexie('article_database');
  db.version(1).stores({
    articles:
      'Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR,Abstract,AuthorsList',
  });
  const articles = db.table('articles');
  const article_local = await articles.get({ DOI });
  article.value = article_local;
});

const corrospondingAuthor = computed(() => {
  const corrospondingAuthor = last(article.value.AuthorsList);
  return corrospondingAuthor;
});
const doiURL = computed(() => {
  return `https://doi.org/${article.value.DOI}`;
});
</script>
