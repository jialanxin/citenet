<template>
  <v-card>
    <v-card-title>
      <v-file-input label="Upload savedrecs.txt" accept=".txt" show-size v-model="value"></v-file-input>
      <v-btn @click="upload">Upload</v-btn>
      <v-spacer />
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
      search: "",
      value: null
    };
  },
  methods: {
    upload: function() {
      let formData = new FormData();
      formData.append("file", this.value);
      formData.append("type", this.value.type);
      axios
        .post("https://api.lxj230.xyz/", formData, {
          headers: {
            accept: "application/json",
            "Content-Type": "multipart/form-data",
            "Access-Control-Allow-Origin": "*"
          }
        })
        .then(response => {
          this.articles=response.data;
        });
    }
  }
};
</script>

<style>
</style>