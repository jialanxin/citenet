<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table :headers="headers" :items="articles" :search="search"></v-data-table>
  </v-card>
</template>

<script>
import axios from "axios";
export default {
  name: "DataTable",
  data: () => {
    return {
      headers: [
        { text: "Title", align: "start", sortable: false, value: "Title" },
        { text: "Year", value: "PY" },
        { text: "LCS", value: "LCS" },
        { text: "GCS", value: "GCS" },
        { text: "LCR", value: "LCR" },
        { text: "CR", value: "CR" }
      ],
      articles: [
        {
          Title: "See this because of request failure",
          PY: 0,
          LCS: 0,
          GCS: 0,
          LCR: 0,
          CR: 0
        }
      ],
      search: ""
    };
  },
  created: function() {
    axios.get("http://citenet.lxj230.xyz/api/").then(response => {
      this.articles = response.data;
    });
  }
};
</script>

<style>
</style>