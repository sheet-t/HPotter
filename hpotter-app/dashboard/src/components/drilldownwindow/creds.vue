<style scoped></style>
<template>
  <v-card class="mx-auto">
    <v-card-text>
      <div class="display-1 font-weight-thin  text-center">Top Credentials</div>
    </v-card-text>
    <v-card-text>
      <ul>
        <li v-for="cred in credslist" v-bind:key="cred">
          username: {{cred.username}}  password: {{cred.password}} count: {{cred.count}}
        </li>
      </ul>
    </v-card-text>
  </v-card>
</template>


<script>
export default{
  computed: {
    credslist() {
      return this.$store.getters.credentials
    }
  }
}
</script>
