<style scoped></style>

<!-- This is the map for "Locations" -->
<template>
  <v-card class="mx-auto">
    <v-card-text>
      <div class="display-1 font-weight-thin  text-center">Map</div>
    </v-card-text>
    <v-card-text>
        <l-map
          style="height: 500px; width: 100%"
          :zoom="zoom"
          :center="center"
          @update:zoom="zoomUpdated"
          @update:center="centerUpdated"
          @update:bounds="boundsUpdated"
        >
          <l-tile-layer :url="url"></l-tile-layer>
          <l-marker v-for="marker in locals" :key="marker" :lat-lng="marker"></l-marker>
        </l-map>
    </v-card-text>
  </v-card>
</template>


<script>
import {LMap, LTileLayer, LMarker } from 'vue2-leaflet';

export default {
    name: 'MyAwesomeMap',
    components: {
        LMap,
        LTileLayer,
        LMarker
    },

  computed: {
    url() {
      return this.$store.getters.url
    },
    zoom() {
      return this.$store.getters.zoom
    },
    center() {
      return this.$store.getters.center
    },
    bounds() {
      return this.$store.getters.bounds
    },
    locals() {
      return this.$store.getters.locals
    }
  },
  methods: {
    zoomUpdated (zoom) {
      this.$store.dispatch('updateZoom', zoom)
    },
    centerUpdated (center) {
      this.$store.dispatch('updateCenter', center)
    },
    boundsUpdated (bounds) {
      this.$store.dispatch('updateBounds', bounds)
    }
  }
}
</script>
