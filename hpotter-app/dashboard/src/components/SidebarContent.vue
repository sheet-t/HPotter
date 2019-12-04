<style scoped>
  .titleDrip {
    position: absolute;
    left: 170px;
    top: 85px;
    z-index: 4;
  }
</style>

<!-- Content of sidebar, use for navigation between v-window items in main content -->
<template>
  <div>
    <v-list nav color="primary">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            <v-img src="../assets/LogoTextWhite.png">&nbsp;</v-img>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <div class="titleDrip">
      <v-img max-width="80" src="../assets/dripnav.png"></v-img>
    </div>

    <v-list>
      <v-list-item-group v-model="item" color="white">
        <v-list-item
          v-for="(item, i) in items"
          v-on:click="updateWindow(i)"
          :key="i">
          <v-list-item-icon>
            <v-icon v-text="item.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="item.text"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </div>
</template>


<script>
  export default {
      data: () => ({
        items: [
          {
            icon: 'mdi-view-dashboard',
            text: 'Dashboard',
          },
          {
            icon: 'mdi-robot',
            text: 'Analytics',
          }
        ],
        item: 0,
      }),
      methods: {
        updateWindow(value) {
          this.$store.dispatch('updateWindow', value)
        }
      }
    }
</script>
