<template>
  <div class="card" :class="colorClass">
    <span class="name">{{build.name}}</span>
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
  font-family: "SourceSansSemi";
  flex: 0 0 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 7px 15px 15px 15px;
}
.card-success {
  background-color: #3AB20C;
}
.card-unknown {
  background-color: #C8CAFF;
}
.card-failure {
  background-color: #CC4B0E;
}
.name {
  font-size: 2.8rem;
}
</style>

