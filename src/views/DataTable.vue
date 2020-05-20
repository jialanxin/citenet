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
    <v-data-table :headers="headers" :items="articles" :search="search" @click:row="clickline"></v-data-table>
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
        { text: "Auther", sortable: false, value: "AU" },
        { text: "Year", value: "PY" },
        { text: "LCS", value: "LCS" },
        { text: "GCS", value: "GCS" },
        { text: "LCR", value: "LCR" },
        { text: "CR", value: "CR" }
      ],
      articles: [
        {
          Title: "See this before request or request failure",
          PY: 0,
          LCS: 0,
          GCS: 0,
          LCR: 0,
          CR: 0,
          DOI: "10.0000/abcdef",
          AU: "Jhon"
        },
        {
          Title: "test row2",
          PY: 10,
          LCS: 10,
          GCS: 10,
          LCR: 10,
          CR: 10,
          DOI: "10.1010/qwerty",
          AU: "Harry"
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
        .post(process.env.VUE_APP_BACKEND_ADDRESS, formData, {
          headers: {
            accept: "application/json",
            "Content-Type": "multipart/form-data",
            "Access-Control-Allow-Origin": "*"
          }
        })
        .then(response => {
          this.articles = response.data;
        });
    },
    clickline: function(payload) {
      let path = "/" + encodeURIComponent(payload.DOI);
      let detailPage = this.$router.resolve({ path: path });
      window.open(detailPage.href, "_blank");
    }
  }
};
</script>

<style>
</style>