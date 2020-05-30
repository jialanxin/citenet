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
