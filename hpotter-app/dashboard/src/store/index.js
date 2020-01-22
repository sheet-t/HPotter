import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        active: 1,
        window: 0,
        content: 0,
        zoom: 2,
        center: [20, 0],
        bounds: null,
        requests: [],
        credentials: [],
        locals: [],
        kpi: [
            { name: 'Attacks', value: 'None', icon: 'mdi-knife-military', id: '1' },
            { name: 'Attack Vectors', value: 'None', icon: 'mdi-directions-fork', id: '2' },
            { name: 'Creds Used', value: 'None', icon: 'mdi-lock-open-outline', id: '3' },
            { name: 'Locations', value: 'None', icon: 'mdi-map-marker', id: '4' }
        ],
        credHeaders: [
            {
              text: "Username",
              align: "left",
              value: "username"
            },
            { 
              text: "Password",
              value: "password"
            }
        ],
        vectorHeaders: [
            {
              text: "Attack Types",
              align: "left",
              value: "name"
            },
            {
              text: "Count",
              value: "number"
            }
        ],
        date: new Date(),
        url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
        viewDate: new Date().toISOString().substr(0, 10),
        weekData: [7, 6, 4, 9, 8, 10, 1],
        labelsWeek: [
            'Sun',
            'Mon',
            'Tue',
            'Wed',
            'Thu',
            'Fri',
            'Sat'
        ],
        valueAttacks: [0, 2, 5, 9, 5, 10, 0, 5],
        labelsAttacks: [
            '12am',
            '3am',
            '6am',
            '9am',
            '12pm',
            '3pm',
            '6pm',
            '9pm'
        ],
        vectors: [
            { name: 'Telnet', port: 23, number: 0 },
            { name: 'ssh', port: 22, number: 0 },
            { name: 'Maria', port: 3306, number: 0 },
            { name: 'http', port: 22, number: 0 },
            { name: 'https', port: 443, number: 0 },
            { name: 'maria_tls', port: 99, number: 0 }
        ]
    },
    getters: {
        requests(state) {
          return state.requests
        },
        credentials(state) {
          return state.credentials
        },
        locals(state) {
          return state.locals
        },
        active(state) {
            return state.active
        },
        window(state) {
            return state.window
        },
        content(state) {
            return state.content
        },
        kpi(state) {
            return state.kpi
        },
        credHeaders(state) {
            return state.credHeaders
        },
        vectorHeaders(state) {
            return state.vectorHeaders
        },
        viewDate(state) {
            return state.viewDate
        },
        weekData(state) {
            return state.weekData
        },
        labelsWeek(state) {
            return state.labelsWeek
        },
        valueAttacks(state) {
            return state.valueAttacks
        },
        labelsAttacks(state) {
            return state.labelsAttacks
        },
        vectors(state) {
            return state.vectors
        },
        url(state) {
            return state.url
        },
        zoom(state) {
            return state.zoom
        },
        center(state) {
          return state.center
        },
        bounds(state) {
          return state.bounds
        }
    },
    mutations: {
        SET_CONNECTIONS(state, promise) {
          var attacks = [0, 0, 0, 0, 0, 0, 0, 0]
          var days = [0, 0, 0, 0, 0, 0, 0]

          var sshhttp = 0
          var telnet = 0
          var maria = 0
          var https = 0
          var mariatls = 0

          promise.json().then( data => {
            for (const conn of data) {
              var connDay = new Date(conn["created_at"])
              var year = connDay.getFullYear()
              var month = connDay.getMonth()
              var day = connDay.getDate()
              var hour = connDay.getHours()
              var dow = connDay.getDay()
              switch (true) {
                case (hour < 3):
                  attacks[0] = attacks[0] + 1
                  break
                case ((hour >= 3) && (hour < 9)):
                  attacks[1] = attacks[1] + 1
                  break
                case ((hour >= 9) && (hour < 12)):
                  attacks[2] = attacks[2] + 1
                  break
                case ((hour >= 12) && (hour < 15)):
                  attacks[3] = attacks[3] + 1
                  break
                case ((hour >= 15) && (hour < 18)):
                  attacks[4] = attacks[4] + 1
                  break
                case ((hour >= 18) && (hour < 21)):
                  attacks[5] = attacks[5] + 1
                  break
                case ((hour >= 21) && (hour < 24)):
                  attacks[6] = attacks[6] + 1
                  break
                default:
                  attacks[7] = attacks[7] + 1
                  break
              }

              switch (conn["destPort"]) {
                case 22:
                  sshhttp = 2
                  state.vectors[1]['number'] = state.vectors[1]['number'] + 1
                  state.vectors[3]['number'] = state.vectors[3]['number'] + 1
                  break
                case 23:
                  telnet = 1
                  state.vectors[0]['number'] = state.vectors[0]['number'] + 1
                  break
                case 3306:
                  maria = 1
                  state.vectors[2]['number'] = state.vectors[2]['number'] + 1
                  break
                case 443:
                  https = 1
                  state.vectors[4]['number'] = state.vectors[4]['number'] + 1
                  break
                case 99:
                  mariatls = 1
                  state.vectors[5]['number'] = state.vectors[5]['number'] + 1
                  break
                default:
                  break
              }

              if ((year == state.date.getFullYear()) && (month == state.date.getMonth())) {
                if ((day - state.date.getDate()) >= (0 - state.date.getDay()) && (day - state.date.getDate()) < (6 - state.date.getDay())) {
                    days[dow] = days[dow] + 1
                }

              }

            }
            state.kpi[0]['value'] = days[state.date.getDay()]
            state.valueAttacks = attacks
            state.weekData = days
            state.kpi[1]['value'] = sshhttp + telnet + maria + https + mariatls
          })
        },
        SET_REQUESTS(state, promise) {
          promise.json().then( data =>
            state.requests = data
          )
        },
        SET_CREDENTIALS(state, promise) {
          let creds = []
          promise.json().then( data => {
            for(let item of data) {
              creds.push(item)
            }
            state.kpi[2]['value'] = data.length
            state.credentials = creds
          })
        },
        SET_LOCALS(state, promise) {
          let locs = []
          let count = 0
          promise.json().then( data => {
            for(let item of data.geometry.coordinates) {
              locs.push(item.reverse())
              count += 1
            }
            state.locals = locs
            state.kpi[3]['value'] = count
          })
        },
        updateActive(state, value) {
            state.active = value
        },
        updateContent(state, value) {
            state.content = value
        },
        updateWindow(state, value) {
            state.window = value
        },
        updateZoom(state, value) {
            state.zoom = value
        },
        updateCenter(state, value) {
            state.center = value
        },
        updateBounds(state, value) {
            state.bounds = value
        }
    },
    actions: {
        SET_CONNECTIONS: async (context) => {
          fetch('http://localhost:8000/connections').then( response => {
            context.commit('SET_CONNECTIONS', response)
          })
        },
        SET_REQUESTS: async (context) => {
          fetch ('http://localhost:8000/requests').then( response => {
            context.commit('SET_REQUESTS', response)
          })
        },
        SET_CREDENTIALS: async (context) => {
          fetch ('http://localhost:8000/credentials').then( response => {
            context.commit('SET_CREDENTIALS', response)
          })
        },
        SET_LOCALS: async (context) => {
          fetch ('http://localhost:8000/connections?geoip=1').then( response => {
            context.commit('SET_LOCALS', response)
          })
        },
        updateActive(context, value) {
            context.commit('updateActive', value)
        },
        updateContent(context, value) {
            context.commit('updateContent', value)
        },
        updateWindow(context, value) {
            context.commit('updateWindow', value)
        },
        updateZoom(context, value) {
            context.commit('updateZoom', value)
        },
        updateCenter(context, value) {
            context.commit('updateCenter', value)
        },
        updateBounds(context, value) {
            context.commit('updateBounds', value)
        }
    }
});
