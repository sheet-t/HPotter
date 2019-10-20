<style scoped>
</style>
<template>
  <v-container>
    <v-layout row wrap ma-2>
      <v-flex>
        <v-window v-bind:value='contentID'>
          <v-window-item value='1'>
            <attacks :valueAttacks="valueAttacks" :labelsAttacks="labelsAttacks" />
          </v-window-item>

          <v-window-item value='2'>
            <vectors />
          </v-window-item>

          <v-window-item value='3'>
            <creds />
          </v-window-item>

          <v-window-item value='4'>
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
    data: () => ({
      valueAttacks: [0, 2, 5, 9, 5, 10, 0, 5],
      labelsAttacks: [
        '12am',
        '3am',
        '6am',
        '9am',
        '12pm',
        '3pm',
        '6pm',
        '9pm',
      ],
      vectors: [
        { name: 'Telnet', port: 23, number: 3 },
        { name: 'ssh', port: 22, number: 7 },
        { name: 'Maria', port: 3306, number: 2 },
        { name: 'http', port: 22, number: 0 },
        { name: 'https', port: 443, number: 18 },
        { name: 'maria_tls', port: 99, number: 4 }
      ],
    }),
    props:['contentID']
  }
</script>
