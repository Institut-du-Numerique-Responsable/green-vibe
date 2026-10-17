<script>
// Fixture: non-conforming Vue
import { createRouter } from 'vue-router';
import Home from '../views/Home.vue';
export default { watch: { payload: { handler() {}, deep: true } } };
</script>
<template>
  <li v-for="(item, index) in items" :key="index">{{ item }}</li>
</template>
