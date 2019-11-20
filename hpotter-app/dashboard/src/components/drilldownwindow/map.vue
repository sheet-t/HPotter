<style scoped></style>
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
          <l-marker v-for="marker in coords" v-bind:key="marker" :lat-lng="marker"></l-marker>
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

  data () {
    return {
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      zoom: 1,
      center: [0, 0],
      bounds: null,
    };
  },
  methods: {
    zoomUpdated (zoom) {
      this.zoom = zoom;
    },
    centerUpdated (center) {
      this.center = center;
    },
    boundsUpdated (bounds) {
      this.bounds = bounds;
    }
  },
  computed: {
    coords(){ return this.$store.getters.locals }
  }
}
</script>
