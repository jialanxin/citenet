<template>
  <div>
    <v-card
      style="z-index: 100; position: fixed"
      height="60"
      width="200"
      class="mt-4"
    >
      <v-text-field
        outlined
        label="Nodes Number"
        v-model="nodeNum"
        @keydown.enter="changeNodeNum"
      />
    </v-card>
    <div id="mountNode" />
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted, onUpdated } from 'vue';
import Dexie from 'dexie';
import { isNotNull } from '../utils/textToArticles';
import { DataSet, Network } from 'vis-network/standalone';

const nodeNum = ref(10);

function processShownArticles(nodeNum, articles_ordered) {
  const shownArticles = articles_ordered.slice(0, nodeNum);
  const nodeList = shownArticles.map((articleUse) => ({
    id: articleUse.DOI,
    label: articleUse.Author,
  }));
  const edgeList = shownArticles.reduce(
    (edgeListacc, articleUse) =>
      edgeListacc.concat(
        articleUse.localCiteList
          .map((localCite) => {
            const articleSource = shownArticles.find(
              (article) => article.DOI === localCite.citeDOI
            );
            if (articleSource !== undefined) {
              return { from: articleUse.DOI, to: articleSource.DOI };
            }
            return null;
          })
          .filter(isNotNull)
      ),
    []
  );
  return { nodes: nodeList, edges: edgeList };
}

const articles_cached = ref([]);

onMounted(async () => {
  const db = new Dexie('article_database');
  db.version(1).stores({
    articles:
      'Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR',
  });
  const articles_table = db.table('articles');
  const articles_unordered = await articles_table.toArray();
  const articles_ordered = articles_unordered.sort((a, b) => {
    if (a.LCR + a.LCS > b.LCR + b.LCS) {
      return -1;
    }
    return 1;
  });
  articles_cached.value = articles_ordered;
  const data = processShownArticles(nodeNum.value, articles_cached.value);
  const container = document.getElementById('mountNode');
  const options = {
    edges: {
      arrows: 'to',
    },
    layout: {
      hierarchical: {
        enabled: true,
        direction: 'DU',
        sortMethod: 'directed',
      },
    },
  };
  const network = new Network(container, data, options);
});
function changeNodeNum() {
  const data = processShownArticles(nodeNum.value, articles_cached.value);
  const container = document.getElementById('mountNode');
  const options = {
    edges: {
      arrows: 'to',
    },
    layout: {
      hierarchical: {
        enabled: true,
        direction: 'DU',
        sortMethod: 'directed',
      },
    },
  };
  const network = new Network(container, data, options);
}
</script>

<style scoped>
#mountNode {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  height: 100%;
  width: 100%;
}
</style>
