<template>
  <div>
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
  </div>
</template>

<script>
import Dexie from "dexie";
export default {
  name: "Details",
  data: () => {
    return {
      article: {
        Title: "Title1",
        Author: "Who1",
        DOI: "10.0000/abcdef",
        Year: 1900,
        Journal: "Nature"
      }
    };
  },
  created: async function() {
    const DOI = this.$route.params.doi;

    const db = new Dexie("article_database");
    db.version(1).stores({
      articles:
        "Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR"
    });

    const article = await db.articles.get({ DOI: DOI });
    this.article = {
      Title: article.Title,
      Author: article.Author,
      DOI: article.DOI,
      Year: article.Year,
      Journal: article.Journal
    };
  },
  computed: {
    doiUrl: function() {
      return `https://doi.org/${this.article.DOI}`;
    }
  }
};
</script>
