<style scoped></style>

<!-- This is the detail window for "attacks" -->
<template>
  <v-card class="mx-auto text-center">
    <v-card-text>
      <!-- TODO: Instead of 24h, this should display the accurate amount of time selected. -->
      <div class="display-1 font-weight-thin">Attacks Last 24h</div>
    </v-card-text>
    <v-card-text>
      <v-sparkline
  :value='valueAttacks' :labels='labelsAttacks' color='white' stroke-linecap='round' show-labels smooth auto-draw></v-sparkline>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <!-- TODO: Wire these up, dynamically adjust time options based on how many days selected. -->
      <v-chip-group color='primary' mandatory>
        <v-chip>
          Past Day
        </v-chip>
        <v-chip>
          Past Hour
        </v-chip>
        <v-chip>
          Past Minute
        </v-chip>
        <v-chip>
          Past Second
        </v-chip>
      </v-chip-group>
    </v-card-actions>
  </v-card>
</template>


<script>
export default{
  computed: {
    valueAttacks() {
      return this.$store.getters.valueAttacks
    },
    labelsAttacks() {
      return this.$store.getters.labelsAttacks
    }
  }
}
</script>
