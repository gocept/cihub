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
      statusColors: {
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
      return this.statusColors[this.build.status]
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
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 7px 15px 15px 15px;
  margin: 5px;
  max-width: 33.3vw;
}
.card-success {
  background-color: rgb(133, 184, 113);
}
.card-unknown {
  background-color: #C8CAFF;
}
.card-failure {
  background-color: rgb(248, 25, 9);
}
.name {
  font-size: 2.8rem;
}
</style>

