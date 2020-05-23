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
    <div id="mountNode" />
  </div>
</template>

<script>
import G6 from "@antv/g6";
import Dexie from "dexie";
export default {
  name: "Graph",
  mounted: async function() {
    if (this.$route.query.nodes == null) {
      this.nodeNum = 10;
    } else {
      this.nodeNum = this.$route.query.nodes;
    }
    const db = new Dexie("article_database");
    db.version(1).stores({
      articles:
        "Title,Journal,GCS,DOI,Year,Author,citeList,LCR,LCS,localCiteList,CR"
    });
    this.articles = await db.articles.toArray();
    this.articles.sort((a, b) => {
      if (a.LCR + a.LCS > b.LCR + b.LCS) {
        return -1;
      } else {
        return 1;
      }
    });

    const shownArticles = this.articles.slice(0, this.nodeNum);
    let node_list = new Array();
    let edge_list = new Array();

    for (let articleUse of shownArticles) {
      node_list.push({ id: articleUse.DOI, label: articleUse.Author });
      for (let localCite of articleUse.localCiteList) {
        for (let articleSource of shownArticles) {
          if (localCite.citeDOI == articleSource.DOI) {
            edge_list.push({
              source: articleUse.DOI,
              target: articleSource.DOI
            });
          }
        }
      }
    }
    this.node_list = node_list;
    this.edge_list = edge_list;

    this.graph = new G6.Graph({
      container: "mountNode",
      width: window.innerWidth,
      height: window.innerHeight - 64,
      fitView: true,
      fitViewPadding: [20, 20, 20, 20],
      layout: {
        type: "dagre",
        preventOverlap: true,
        rankdir: "BT"
      },
      defaultNode: {
        size: 50,
        style: {},
        labelCfg: {
          style: {
            stroke: "none",
            fill: "black"
          }
        }
      },
      defaultEdge: {
        style: {
          endArrow: true,
          opacity: 1,
          stroke: "black"
        }
      },
      modes: {
        default: ["drag-canvas", "zoom-canvas"] // 允许拖拽画布、放缩画布、拖拽节点
      }
    });
    this.graph.data({ nodes: this.node_list, edges: this.edge_list });
    this.graph.render();
    this.graph.on("node:click", e => {
      const clickNodes = this.graph.findAllByState("node", "click");
      clickNodes.forEach(cn => {
        this.graph.setItemState(cn, "click", false);
      });
      const nodeItem = e.item;
      this.graph.setItemState(nodeItem, "click", true);
      const detailPage = this.$router.resolve({
        name: "Details",
        params: { doi: nodeItem._cfg.id }
      });
      window.open(detailPage.href, "_blank");
    });
  },
  methods: {
    changeNodeNum: async function() {
      this.$router.replace({ name: "Graph", query: { nodes: this.nodeNum } });
      const shownArticles = this.articles.slice(0, this.nodeNum);
      let node_list = new Array();
      let edge_list = new Array();

      for (let articleUse of shownArticles) {
        node_list.push({ id: articleUse.DOI, label: articleUse.Author });
        for (let localCite of articleUse.localCiteList) {
          for (let articleSource of shownArticles) {
            if (localCite.citeDOI == articleSource.DOI) {
              edge_list.push({
                source: articleUse.DOI,
                target: articleSource.DOI
              });
            }
          }
        }
      }
      this.node_list = node_list;
      this.edge_list = edge_list;
      this.graph.data({ nodes: this.node_list, edges: this.edge_list });
      this.graph.render();
    }
  },
  data: () => {
    return {
      nodeNum: 10,
      articles: [],
      graph: null,
      node_list: [
        {
          id: "10.1038/NNANO.2014.167",
          label: "See these before request or request failure",
          lcs: 3
        },
        {
          id: "10.1103/PhysRevLett.108.196802",
          label: "Test Node",
          lcs: 3
        },
        {
          id: "10.1063/1.125474",
          label: "Test Node",
          lcs: 2
        },
        {
          id: "10.1021/nn303973r",
          label: "Test Node",
          lcs: 2
        },
        {
          id: "10.1021/nn404013d",
          label: "Test Node",
          lcs: 2
        },
        {
          id: "10.1126/science.1235547",
          label: "Test Node",
          lcs: 2
        },
        {
          id: "10.1021/nl302015v",
          label: "Test Node",
          lcs: 1
        },
        {
          id: "10.1063/1.4922729",
          label: "Test Node",
          lcs: 1
        },
        {
          id: "10.1126/sciadv.1601741",
          label: "Test Node",
          lcs: 1
        },
        {
          id: "10.1063/1.1376663",
          label: "Test Node",
          lcs: 1
        },
        {
          id: "10.1126/science.aao3503",
          label: "Test Node",
          lcs: 0
        },
        {
          id: "10.1038/s41598-018-20810-6",
          label: "Test Node",
          lcs: 0
        },
        {
          id: "10.1126/sciadv.1700518",
          label: "Test Node",
          lcs: 0
        },
        {
          id: "10.1364/OL.44.004103",
          label: "Test Node",
          lcs: 0
        }
      ],
      edge_list: [
        {
          source: "10.1126/sciadv.1601741",
          target: "10.1063/1.4922729"
        },
        {
          source: "10.1126/science.aao3503",
          target: "10.1038/NNANO.2014.167"
        },
        {
          source: "10.1126/sciadv.1601741",
          target: "10.1038/NNANO.2014.167"
        },
        {
          source: "10.1126/sciadv.1700518",
          target: "10.1038/NNANO.2014.167"
        },
        {
          source: "10.1126/sciadv.1601741",
          target: "10.1021/nn404013d"
        },
        {
          source: "10.1063/1.4922729",
          target: "10.1021/nn404013d"
        },
        {
          source: "10.1126/sciadv.1601741",
          target: "10.1126/science.1235547"
        },
        {
          source: "10.1038/NNANO.2014.167",
          target: "10.1126/science.1235547"
        },
        {
          source: "10.1038/s41598-018-20810-6",
          target: "10.1021/nn303973r"
        },
        {
          source: "10.1038/NNANO.2014.167",
          target: "10.1021/nn303973r"
        },
        {
          source: "10.1063/1.4922729",
          target: "10.1021/nl302015v"
        },
        {
          source: "10.1126/science.aao3503",
          target: "10.1103/PhysRevLett.108.196802"
        },
        {
          source: "10.1038/s41598-018-20810-6",
          target: "10.1103/PhysRevLett.108.196802"
        },
        {
          source: "10.1126/sciadv.1700518",
          target: "10.1103/PhysRevLett.108.196802"
        },
        {
          source: "10.1364/OL.44.004103",
          target: "10.1063/1.1376663"
        },
        {
          source: "10.1364/OL.44.004103",
          target: "10.1063/1.125474"
        },
        {
          source: "10.1063/1.1376663",
          target: "10.1063/1.125474"
        }
      ]
    };
  }
};
</script>

<style>
</style>