<template>
  <div id="app">
    <auth-view v-if="!loggedIn" @loggedIn="updateLogInStatus"></auth-view>
    <div v-if="loggedIn">
      <div class="build-summary">
        <div>Last fetch: {{lastFetch}}</div>
      </div>
      <build-overview>
        <build-card v-for="build in failed" :key="build.name" :build="build">
        </build-card>
      </build-overview>
      <build-overview>
        <build-card v-for="build in unknown" :key="build.name" :build="build">
        </build-card>
      </build-overview>
      <build-overview>
        <build-card v-for="build in succeded" :key="build.name" :build="build">
        </build-card>
      </build-overview>
    </div>
  </div>
</template>

<script>
import AuthView from './components/AuthView.vue'
import BuildCard from './components/BuildCard.vue'
import BuildOverview from './components/BuildOverview.vue'
import { setInterval } from 'timers';
import moment from 'moment';

export default {
  name: 'app',
  components: {
    AuthView,
    BuildOverview,
    BuildCard
  },
  data() {
    return {
      builds: [],
      loggedIn: false,
      lastFetch: null
    }
  },
  methods: {
    fetchBuilds() {
      if (this.loggedIn) {
        return this.$getBuilds().then((resp) => {
          this.builds = resp.data;
          this.lastFetch = moment().format('HH:mm DD.MM.YYYY');
        });
      }
    },
    updateLogInStatus(event) {
      this.loggedIn = event;
      if (event) {
        this.fetchBuilds();
      }
    }
  },
  mounted() {
    setInterval(this.fetchBuilds, 60000);
  },
  computed: {
    failed() {
      return this.builds.filter(x => x.status === 'Failure')
    },
    unknown() {
      return this.builds.filter(x => x.status === 'Unknown')
    },
    succeded() {
      return this.builds.filter(x => x.status === 'Success')
    }
  }
}
</script>

<style>
body {
  font-family: "SourceSans";
  background-color: #fcf6ec
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
  display: flex;
  flex-direction: row;
  padding-bottom: 30px;
  font-family:"SourceSansSemi";
  font-size: 3rem;
}
.build-summary > div {
  margin-right: 20px;
}
</style>
