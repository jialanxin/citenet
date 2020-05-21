<template>
  <div>
    <v-simple-table>
      <template>
        <tbody>
          <tr>
            <td>Title</td>
            <td>{{article.Title}}</td>
          </tr>
          <tr>
            <td>Author</td>
            <td>{{article.Author}}</td>
          </tr>
          <tr>
            <td>Year</td>
            <td>{{article.Year}}</td>
          </tr>
          <tr>
            <td>Journal</td>
            <td>{{article.Journal}}</td>
          </tr>
          <tr>
            <td>DOI</td>
            <td>
              <a :href="this.doiUrl">{{article.DOI}}</a>
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script>
import axios from "axios";
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
  created: function() {
    axios
      .get(process.env.VUE_APP_BACKEND_ADDRESS + this.$route.path)
      .then(response => {
        this.article = response.data;
      });
  },
  computed: {
    doiUrl: function() {
      return `https://doi.org/${this.article.DOI}`;
    }
  }
};
</script>
