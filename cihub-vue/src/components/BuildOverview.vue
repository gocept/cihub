<template>
  <div class="build-overview">
      <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'BuildOverview'
}
</script>

<style scoped>
.build-overview {
  display: flex;
  flex-wrap: wrap;
  padding: 30px 0;
}
</style>

