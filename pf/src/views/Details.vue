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
            <a :href="this.doiUrl">{{ article.DOI }}</a>
          </td>
        </tr>
        <tr>
          <td>Abstract</td>
          <td>
            {{article.Abstract}}
          </td>
        </tr>
        <tr>
          <td>Local Cites</td>
          <td>
            <p v-for="cite in article.localCiteList" :key="cite.citeDOI">
              <a target="_blank" :href="jumpToCite(cite.citeDOI)">
              {{cite.citeTitle}}
              </a></p>
          </td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Dexie from 'dexie';
import last from 'lodash/last';
import { Article } from '../logic/textToArticles';

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
    Abstract: 'Abstract1',
    AuthorsList: [],
  };

  private get doiUrl(): string {
    return `https://doi.org/${this.article.DOI}`;
  }

  private async created(): Promise<void> {
    const DOI = this.$route.params.doi;
    const db = new Dexie('article_database');
    db.version(1).stores({
      articles:
        'Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR,Abstract,AuthorsList',
    });
    const articles = db.table('articles');
    const article = await articles.get({ DOI });
    this.article = article;
  }

  private get corrospondingAuthor(): string {
    const corrospondingAuthor = last(this.article.AuthorsList);
    if (typeof corrospondingAuthor === 'undefined') {
      return 'Corrosponding Author Not Found';
    }
    return corrospondingAuthor;
  }

  private jumpToCite(citeDoi: string): string {
    const detailPage = this.$router.resolve({
      name: 'Details',
      params: { doi: citeDoi },
    });
    return detailPage.href;
  }
}
</script>

<style>
</style>
