<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <span>CiteNet</span>
      </div>
      <v-spacer></v-spacer>
      <v-btn @click="clickGraph" prepend-icon="mdi-graph"> Graph </v-btn>
      <v-btn
        href="https://e0925574.tk/posts/IntroCiteNet"
        target="_blank"
        prepend-icon="mdi-help-circle-outline"
      >
        Usage
      </v-btn>
      <v-btn
        href="https://github.com/jialanxin/citenet/issues"
        prepend-icon="mdi-bug"
        target="_blank"
      >
        Report Bugs
      </v-btn>
    </v-app-bar>
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script lang="ts" setup>
import router from './router';
function clickGraph() {
  const graphPage = router.resolve({ name: 'Graph' });
  window.open(graphPage.href, '_blank');
}
</script>
