<template>
  <div id="app">
    <div class="build-summary">
      <span>Failures: {{failed.length}}</span>
      <span>Unknown: {{unknown.length}}</span>
    </div>
    <build-overview>
      <build-card v-for="build in builds" :key="build.name" :build="build">
      </build-card>
    </build-overview>
  </div>
</template>

<script>
import axios from 'axios'
import BuildCard from './components/BuildCard.vue'
import BuildOverview from './components/BuildOverview.vue'

export default {
  name: 'app',
  components: {
    BuildOverview,
    BuildCard
  },
  data() {
    return {
      builds: [],
      baseUrl: 'http://127.0.0.1:8080/api'
    }
  },
  created() {
    this.getBuilds().then((resp) => {
      this.builds = resp.data
    });
  },
  methods: {
    getBuilds() {
      return axios.get(`${this.baseUrl}/cc.json`)
    }
  },
  computed: {
    failed() {
      return this.builds.filter(x => x.status === 'Failure')
    },
    unknown() {
      return this.builds.filter(x => x.status === 'Unknown')
    }
  }
}
</script>

<style>
body {
  font-family: "SourceSans";
  background-color: #f5f5f5
}
</style>

<style scoped>
@font-face {
    font-family: SourceSans;
    src: url("assets/fonts/SourceSansPro-Regular.otf") format("opentype");
}
@font-face {
    font-family: SourceSansSemi;
    src: url("assets/fonts/SourceSansPro-Semibold.otf") format("opentype");
}
@font-face {
    font-family: SourceSansBold;
    src: url("assets/fonts/SourceSansPro-Bold.otf") format("opentype");
}
.build-summary {
  font-family:"SourceSansSemi";
  font-size: 3rem;
}
</style>
