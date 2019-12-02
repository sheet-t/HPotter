<style scoped>
</style>
<template>
  <v-container>
    <v-layout row wrap ma-2>
      <v-flex>
        <v-window :value="content">
          <v-window-item>
            <attacks :valueAttacks="valueAttacks" :labelsAttacks="labelsAttacks" />
          </v-window-item>

          <v-window-item value="2">
            <vectors />
          </v-window-item>

          <v-window-item value="3">
            <creds />
          </v-window-item>

          <v-window-item value="4">
            <IPmap />
          </v-window-item>
        </v-window>
      </v-flex>
    </v-layout>
  </v-container>
</template>


<script>
  import attacks from './drilldownwindow/attacks';
  import vectors from './drilldownwindow/vectors';
  import creds from './drilldownwindow/creds';
  import IPmap from './drilldownwindow/map';

  export default{
  components: {
    attacks,
    vectors,
    creds,
    IPmap
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
