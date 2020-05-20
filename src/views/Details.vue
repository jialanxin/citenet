<template>
  <div class="about">
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
            <td>DOI</td>
            <td>{{article.DOI}}</td>
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
        DOI: "10.0000/abcdef"
      }
    };
  },
  created: function() {
    axios.get(process.env.VUE_APP_BACKEND_ADDRESS + this.$route.path).then(response => {
      this.article = response.data;
    });
  }
};
</script>
