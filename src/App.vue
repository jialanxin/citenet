<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <span>CiteNet</span>
    </v-app-bar>

    <v-content>
     <router-view />
    </v-content>
  </v-app>
</template>

<script>

export default {
  name: 'App',



  data: () => ({
    //
  }),
};
</script>
