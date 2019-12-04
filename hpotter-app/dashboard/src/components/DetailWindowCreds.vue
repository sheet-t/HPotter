<style scoped></style>

<!-- This is the detail window for "Creds Used" -->
<template>
  <v-card class="mx-auto">
    <v-card-text>
      <div class="display-1 font-weight-thin  text-center">Credentials Used</div>
    </v-card-text>
    <v-card-text>
      <v-data-table
        :headers="credHeaders"
        :items="credslist"
      ></v-data-table>
    </v-card-text>
  </v-card>
</template>


<script>
export default{
  computed: {
    credslist() {
      return this.$store.getters.credentials
    },
    credHeaders() {
      return this.$store.getters.credHeaders
    }
  }
}
</script>
