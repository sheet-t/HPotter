<style scoped>
</style>

<!-- This is a strip that spawns a card for each statistic -->
<template>
  <v-container class="pt-0 mt-0">
    <v-layout row wrap>
      <v-flex xs3 v-for="stat in kpi" :key="stat.id">
        <CardStripCard :kpi="stat" v-on:update:content="updateContent(stat.id)" :active="active"/>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import CardStripCard from './CardStripCard';

  export default {
    components: {
      CardStripCard,
    },
    computed: {
      content() {
        return this.$store.getters.content
      },
      kpi() {
        return this.$store.getters.kpi
      },
      active() {
        return this.$store.getters.active
      }
    },
    methods: {
      updateContent(content) {
        this.$store.dispatch('updateContent', content)
        this.$store.dispatch('updateActive', content)
      }
    }
  }
</script>
