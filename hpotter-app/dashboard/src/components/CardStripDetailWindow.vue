<style scoped>
</style>

<!-- Detail window for the currently selected statistic in CardStrip. -->
<template>
  <v-container>
    <v-layout row wrap ma-2>
      <v-flex>
        <v-window :value="content">
          <v-window-item>
            <DetailWindowAttacks :valueAttacks="valueAttacks" :labelsAttacks="labelsAttacks" />
          </v-window-item>

          <v-window-item value="2">
            <DetailWindowVectors />
          </v-window-item>

          <v-window-item value="3">
            <DetailWindowCreds />
          </v-window-item>

          <v-window-item value="4">
            <DetailWindowLocation />
          </v-window-item>
        </v-window>
      </v-flex>
    </v-layout>
  </v-container>
</template>


<script>
  import DetailWindowAttacks from './DetailWindowAttacks';
  import DetailWindowVectors from './DetailWindowVectors';
  import DetailWindowCreds from './DetailWindowCreds';
  import DetailWindowLocation from './DetailWindowLocation';

  export default{
  components: {
    DetailWindowAttacks,
    DetailWindowVectors,
    DetailWindowCreds,
    DetailWindowLocation
    },
    computed: {
      content() {
        return this.$store.getters.content
      },
      valueAttacks() {
        return this.$store.getters.valueAttacks
      },
      labelsAttacks() {
        return this.$store.getters.labelsAttacks
      },
      vectors() {
        return this.$store.getters.vectors
      }
    },
    data: () => ({}),
  }
</script>
