<template>
  <div class="card" :class="colorClass">
    <span>{{build.name}}</span>
    <span>{{time}} {{date}}</span>
    <a :href="build.url"><span>{{build.buildnumber}}</span></a>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'BuildCard',
  data() {
    return {
      colors: {
        Success: 'card-success',
        Unknown: 'card-unknown',
        Failure: 'card-failure'
      },
      dateObject: moment(this.build.timestamp),
    }
  },
  props: {
    build: {
      type: Object,
      required: true
    }
  },
  computed: {
    colorClass() {
      return this.colors[this.build.status]
    },
    date() {
      return this.dateObject.format('hh:mm')
    },
    time() {
      return this.dateObject.format('DD.MM.YYYY')
    }
  }
}
</script>
<style scoped>
.card {
  flex: 0 0 200px;
  display: flex;
  flex-direction: column;
}
.card-success {
  background-color: green;
}
.card-unknown {
  background-color: yellow;
}
.card-failure {
  background-color: red;
}
</style>

