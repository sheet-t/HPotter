<style>

  /* Global Page Style
  Note that we are not using the standard vuetify grey theme.
  New components created may require individual CSS rules to
  not be a different shade of gray */

  .theme--dark.v-application {
    background: #2B3648 !important;
}
  .theme--dark.v-sheet {
  background-color: #212936 !important;
  border-color: #212936 !important;
}
  .slateNav {
    background-color: #212936 !important;
}
  .hiddenNav {
  background-color: rgba(0,0,0,0) !important;
}
  .theme--dark.v-picker__body{
  background: #212936 !important;
}
  .theme--dark.v-card {
    background-color: #212936 !important;
}
  .theme--dark.v-chip:not(.v-chip--active) {
  background: #293245;
}
  .theme--dark.v-data-table {
    background: #212936;
  }
</style>


<template>
  <v-app>
    <!--Left Sidebar, Navigation-->
    <v-navigation-drawer floating app class="elevation-3 slateNav">
      <SidebarContent :window="window"/>
    </v-navigation-drawer>
    <!--End Sidebar-->

    <!--Large View Right Hand Content-->
    <v-navigation-drawer floating right app width="300px" class="hiddenNav">
      <div class="mt-8">
        <!-- TODO: Datepicker should be able to select ranges of days -->
        <v-date-picker v-model="viewDate"></v-date-picker>
      </div>
      <br />
      <v-card class="mr-2 text-center">
        <v-card-title>
        Activity
        </v-card-title>
        <v-card-text>
          <v-sparkline :value="weekData" :labels="labelsWeek" line-width="10"  stroke-linecap="round" type="bars" color="white" show-labels smooth auto-draw></v-sparkline>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>
    <!--End Right Hand Content-->

    <v-content>
      <v-container ma-2>
        <v-row>
          <v-col>

            <!--Main Content-->
            <v-window v-model='window'>

              <!--Dashboard-->
              <v-window-item>
                <v-row>
                  <CardStrip :kpi="kpi" :content="content" />
                </v-row>

                <v-row>
                  <CardStripDetailWindow :content="content" :valueAttacks="valueAttacks" :labelsAttacks="labelsAttacks" :vectors="vectors"/>
                </v-row>
              </v-window-item>


              <!--Analytics-->
              <v-window-item>
                <v-card>
                  <v-card-text>
                    <!-- TODO: Full Display of output of ML Algorithm. -->
                    Analytics Component Here
                  </v-card-text>
                </v-card>
              </v-window-item>


            </v-window>
            <!--End Main Content-->

          </v-col>

          <!-- Floating datepicker for small screens -->
          <v-dialog v-model="dialog" width="300">
            <template v-slot:activator="{ on }">
              <v-fab-transition><v-btn v-on="on" v-show="$vuetify.breakpoint.mdAndDown" fixed dark fab bottom right color="primary"><v-icon>mdi-calendar</v-icon></v-btn></v-fab-transition>
            </template>
            <v-date-picker v-model="viewDate"></v-date-picker>
          </v-dialog>
          <!-- End Floating datepicker -->

        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>

import SidebarContent from './components/SidebarContent';
import CardStrip from './components/CardStrip';
import CardStripDetailWindow from './components/CardStripDetailWindow';

export default {



  name: 'App',
  components: {
    SidebarContent,
    CardStrip,
    CardStripDetailWindow
  },
  data: () => ({
    viewDate: new Date().toISOString().substr(0, 10)
  }),
  methods: {

  },
  computed: {
    loadconnections() {
      return this.$store.getters.connections
    },
    loadrequests() {
      return this.$store.getters.requests
    },
    loadcredentials() {
      return this.$store.getters.credentials
    },
    loadlocals() {
      return this.$store.getters.locals
    },
    content() {
      return this.$store.getters.content
    },
    window() {
      return this.$store.getters.window
    },
    kpi() {
      return this.$store.getters.kpi
    },
    weekData() {
      return this.$store.getters.weekData
    },
    labelsWeek() {
      return this.$store.getters.labelsWeek
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

  created () {
    this.$store.dispatch('SET_CONNECTIONS')
    this.$store.dispatch('SET_REQUESTS')
    this.$store.dispatch('SET_CREDENTIALS')
    this.$store.dispatch('SET_LOCALS')
    this.$vuetify.theme.dark = true
  },
};
</script>
