<template>
  <div>
    <v-card
      style="z-index:100;position:fixed"
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
    <div id="mountNode"/>
  </div>
</template>

<script lang='ts'>
import { Component, Vue } from 'vue-property-decorator';
import Dexie from 'dexie';
import { Graph } from '@antv/g6/lib';
import { NodeConfig, EdgeConfig } from '@antv/g6/lib/types';
import { Article, isNotNull } from './DataTable.vue';

interface Node {
  id: string;
  label: string;
}

interface Edge {
  source: string;
  target: string;
}

@Component
export default class GraphPage extends Vue {
  private async processShownArticles(nodeNum: number): Promise<void> {
    const shownArticles = this.articles.slice(0, nodeNum);
    const nodeList: NodeConfig[] = shownArticles.map((articleUse) => ({
      id: articleUse.DOI,
      label: articleUse.Author,
    }));
    const edgeList: EdgeConfig[] = shownArticles.reduce(
      (edgeListacc: EdgeConfig[], articleUse: Article) => edgeListacc.concat(
        articleUse.localCiteList
          .map((localCite) => {
            const articleSource: Article|undefined = shownArticles.find(
              (article) => article.DOI === localCite.citeDOI,
            );
            if (articleSource !== undefined) {
              return { source: articleUse.DOI, target: articleSource.DOI };
            }
            return null;
          })
          .filter(isNotNull),
      ),
      [],
    );
    this.nodeList = nodeList;
    this.edgeList = edgeList;
  }

  private async mounted(): Promise<void> {
    if (this.$route.query.nodes == null) {
      this.nodeNum = 10;
    } else {
      this.nodeNum = parseInt(this.$route.query.nodes as string, 10);
    }
    const db = new Dexie('article_database');
    db.version(1).stores({
      articles:
        'Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR',
    });
    const articles = db.table('articles');
    this.articles = await articles.toArray();
    this.articles.sort((a, b) => {
      if (a.LCR + a.LCS > b.LCR + b.LCS) {
        return -1;
      }
      return 1;
    });
    await this.processShownArticles(this.nodeNum);
    this.graph = new Graph({
      container: 'mountNode',
      width: window.innerWidth,
      height: window.innerHeight - 64,
      fitView: true,
      fitViewPadding: [20, 20, 20, 20],
      layout: {
        type: 'dagre',
        preventOverlap: true,
        rankdir: 'BT',
      },
      defaultNode: {
        size: 50,
        style: {},
        labelCfg: {
          style: {
            stroke: 'none',
            fill: 'black',
          },
        },
      },
      defaultEdge: {
        style: {
          endArrow: true,
          opacity: 1,
          stroke: 'black',
        },
      },
      modes: {
        default: ['drag-canvas', 'zoom-canvas'], // 允许拖拽画布、放缩画布、拖拽节点
      },
    });
    this.graph.data({ nodes: this.nodeList, edges: this.edgeList });
    this.graph.render();
    this.graph.on('node:click', (e: any) => {
      const clickNodes = this.graph.findAllByState('node', 'click');
      clickNodes.forEach((cn) => {
        this.graph.setItemState(cn, 'click', false);
      });
      const nodeItem = e.item;
      this.graph.setItemState(nodeItem, 'click', true);
      const clicked = this.graph.findAllByState('node', 'click')[0];
      const doi: string = clicked.getID();
      const detailPage = this.$router.resolve({
        name: 'Details',
        params: { doi },
      });
      window.open(detailPage.href, '_blank');
    });
  }

  private changeNodeNum(): void{
    this.$router.replace({ name: 'Graph', query: { nodes: this.nodeNum.toString(10) } });
    this.processShownArticles(this.nodeNum);
    this.graph.data({ nodes: this.nodeList, edges: this.edgeList });
    this.graph.render();
  }


  nodeNum = 10;

  articles: Article[] = [];

  graph: Graph = new Graph({
    container: 'mountNode',
    width: window.innerWidth,
    height: window.innerHeight - 64,
  });

  nodeList: NodeConfig[] = [
    {
      id: '10.1038/NNANO.2014.167',
      label: 'See these before request or request failure',
    },
    {
      id: '10.1103/PhysRevLett.108.196802',
      label: 'Test Node',
    },
    {
      id: '10.1063/1.125474',
      label: 'Test Node',
    },
    {
      id: '10.1021/nn303973r',
      label: 'Test Node',
    },
    {
      id: '10.1021/nn404013d',
      label: 'Test Node',
    },
    {
      id: '10.1126/science.1235547',
      label: 'Test Node',
    },
    {
      id: '10.1021/nl302015v',
      label: 'Test Node',
    },
    {
      id: '10.1063/1.4922729',
      label: 'Test Node',
    },
    {
      id: '10.1126/sciadv.1601741',
      label: 'Test Node',
    },
    {
      id: '10.1063/1.1376663',
      label: 'Test Node',
    },
    {
      id: '10.1126/science.aao3503',
      label: 'Test Node',
    },
    {
      id: '10.1038/s41598-018-20810-6',
      label: 'Test Node',
    },
    {
      id: '10.1126/sciadv.1700518',
      label: 'Test Node',
    },
    {
      id: '10.1364/OL.44.004103',
      label: 'Test Node',
    },
  ];

  edgeList: EdgeConfig[] = [
    {
      source: '10.1126/sciadv.1601741',
      target: '10.1063/1.4922729',
    },
    {
      source: '10.1126/science.aao3503',
      target: '10.1038/NNANO.2014.167',
    },
    {
      source: '10.1126/sciadv.1601741',
      target: '10.1038/NNANO.2014.167',
    },
    {
      source: '10.1126/sciadv.1700518',
      target: '10.1038/NNANO.2014.167',
    },
    {
      source: '10.1126/sciadv.1601741',
      target: '10.1021/nn404013d',
    },
    {
      source: '10.1063/1.4922729',
      target: '10.1021/nn404013d',
    },
    {
      source: '10.1126/sciadv.1601741',
      target: '10.1126/science.1235547',
    },
    {
      source: '10.1038/NNANO.2014.167',
      target: '10.1126/science.1235547',
    },
    {
      source: '10.1038/s41598-018-20810-6',
      target: '10.1021/nn303973r',
    },
    {
      source: '10.1038/NNANO.2014.167',
      target: '10.1021/nn303973r',
    },
    {
      source: '10.1063/1.4922729',
      target: '10.1021/nl302015v',
    },
    {
      source: '10.1126/science.aao3503',
      target: '10.1103/PhysRevLett.108.196802',
    },
    {
      source: '10.1038/s41598-018-20810-6',
      target: '10.1103/PhysRevLett.108.196802',
    },
    {
      source: '10.1126/sciadv.1700518',
      target: '10.1103/PhysRevLett.108.196802',
    },
    {
      source: '10.1364/OL.44.004103',
      target: '10.1063/1.1376663',
    },
    {
      source: '10.1364/OL.44.004103',
      target: '10.1063/1.125474',
    },
    {
      source: '10.1063/1.1376663',
      target: '10.1063/1.125474',
    },
  ];
}
</script>

<style>
</style>
