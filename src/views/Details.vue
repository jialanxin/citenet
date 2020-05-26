<template>
  <v-simple-table>
    <template>
      <tbody>
        <tr>
          <td>Title</td>
          <td>{{ article.Title }}</td>
        </tr>
        <tr>
          <td>Author</td>
          <td>{{ article.Author }}</td>
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
          <td>DOI</td>
          <td>
            <a :href="this.doiUrl">{{ article.DOI }}</a>
          </td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Dexie from 'dexie';
import { Article } from './DataTable.vue';

@Component
export default class Details extends Vue {
  article: Article = {
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
  };

  private get doiUrl(): string {
    return `https://doi.org/${this.article.DOI}`;
  }

  private async created(): Promise<void> {
    const DOI = this.$route.params.doi;
    const db = new Dexie('article_database');
    db.version(1).stores({
      articles:
        'Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR',
    });
    const articles = db.table('articles');
    const article = await articles.get({ DOI });
    this.article = article;
  }
}
</script>

<style>
</style>
