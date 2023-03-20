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
import { ref,Ref, onMounted, onUpdated } from 'vue';
import { useRouter } from 'vue-router';
import Dexie from 'dexie';
import { Article } from '../utils/textToArticles';
import { DataSet, Network } from 'vis-network/standalone';

const nodeNum = ref(10);
const router = useRouter();

function processShownArticles(nodeNum: number, articles_ordered:Article[]) {
  const shownArticles = articles_ordered.slice(0, nodeNum);
  const nodeList = shownArticles.map((articleUse) => ({
    id: articleUse.DOI,
    label: articleUse.Author,
  }));
  const edgeList = []
  for (let articleUse of shownArticles){
    for (let localCite of articleUse.localCiteList){
      const articleSource = shownArticles.find((article)=>article.DOI==localCite.citeDOI)
      if (articleSource !== undefined){
        edgeList.push({from: articleUse.DOI, to: articleSource.DOI})
      }
    }
  }
  return { nodes: nodeList, edges: edgeList };
}

const articles_cached:Ref<Article[]> = ref([]);

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
    physics: false,
    edges: {
      arrows: 'to',
    },
    layout: {
      hierarchical: {
        levelSeparation: 100,
        enabled: true,
        direction: 'DU',
        sortMethod: 'directed',
        nodeSpacing: 150,
      },
    },
  };
  if (container !== null ){
    const network = new Network(container, data, options);
    network.on('click', function (params) {
    clickNode(params);
  });
  }

});
function clickNode(params:any) {
  const nodes = params.nodes;
  if (nodes?.length>0) {
    const node_DOI = nodes[0];
    const DOIBase64 = btoa(node_DOI);
    const detailPage = router.resolve({
      name: 'Details',
      params: { doi: DOIBase64 },
    });
    window.open(detailPage.href, '_blank');
  }
}
function changeNodeNum() {
  const data = processShownArticles(nodeNum.value, articles_cached.value);
  const container = document.getElementById('mountNode');
  const options = {
    physics: false,
    edges: {
      arrows: 'to',
    },
    layout: {
      hierarchical: {
        enabled: true,
        direction: 'DU',
        sortMethod: 'directed',
        levelSeparation: 100,
        nodeSpacing: 150,
      },
    },
  };
  if (container !== null ){
    const network = new Network(container, data, options);
    network.on('click', function (params) {
    clickNode(params);
  });
  }
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
