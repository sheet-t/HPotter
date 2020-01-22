<style scoped></style>

<!-- This is the detail window for "Attack Vectors" -->
<template>
  <v-card class="mx-auto">
    <v-card-text>
      <div class="display-1 font-weight-thin  text-center">Attack Vectors</div>
    </v-card-text>
    <v-card-text>
      <v-data-table
        :headers="vectorHeaders"
        :items="vectors"
      ></v-data-table>
    </v-card-text>
  </v-card>
</template>


<script>
export default{
  computed: {
    vectors() {
      return this.$store.getters.vectors
    },
    vectorHeaders() {
      return this.$store.getters.vectorHeaders
    }
  }
}
</script>
