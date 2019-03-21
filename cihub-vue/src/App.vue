<template>
  <div id="app">
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
  }
}
</script>