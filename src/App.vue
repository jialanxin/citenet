<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <span>CiteNet</span>

      </div>

      <v-spacer></v-spacer>
        <v-btn @click=clickGraph  text>
          <v-icon>mdi-graph</v-icon>
          Graph
        </v-btn>
        <v-btn href="https://lxj230.xyz/posts/IntroCiteNet" target="_blank" text>
          <v-icon>mdi-help-circle-outline</v-icon>
          Usage
        </v-btn>
        <v-btn href="https://github.com/jialanxin/citenet/issues" target="_blank" text>
          <v-icon>mdi-bug</v-icon>
          Report Bugs
        </v-btn>

    </v-app-bar>

    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'App',

  data: () => ({
    //
  }),
  methods: {
    clickGraph() {
      const graphPage = this.$router.resolve({ name: 'Graph' });
      window.open(graphPage.href, '_blank');
    },
  },
});
</script>
