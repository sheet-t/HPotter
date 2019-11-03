import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        active: 1,
        window: 0,
        content: 1,
        connections: [],
        requests: [],
        credentials: [],
        locals: [],
        kpi: [
            { name: 'Attacks', value: '128', icon: 'mdi-knife-military', id: '1' },
            { name: 'Attack Vectors', value: '6', icon: 'mdi-directions-fork', id: '2' },
            { name: 'Creds Used', value: '29', icon: 'mdi-lock-open-outline', id: '3' },
            { name: 'Countries', value: '5', icon: 'mdi-map-marker', id: '4' }
        ],
        viewDate: new Date().toISOString().substr(0, 10),
        weekData: [7, 6, 4, 9, 8, 10, 1],
        labelsWeek: [
            'Mon',
            'Tue',
            'Wed',
            'Thu',
            'Fri',
            'Sat',
            'Sun'
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
            { name: 'Telnet', port: 23, number: 3 },
            { name: 'ssh', port: 22, number: 7 },
            { name: 'Maria', port: 3306, number: 2 },
            { name: 'http', port: 22, number: 0 },
            { name: 'https', port: 443, number: 18 },
            { name: 'maria_tls', port: 99, number: 4 }
        ]
    },
    getters: {
        connections(state) {
          return state.connections
        },
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
        }
    },
    mutations: {
        SET_CONNECTIONS(state, value) {
          state.connections = value
        },
        SET_REQUESTS(state, value) {
          state.requests = value
        },
        SET_CREDENTIALS(state, value) {
          state.credentials = value
        },
        SET_LOCALS(state, value) {
          state.locals = value
        },
        updateActive(state, value) {
            state.active = value
        },
        updateContent(state, value) {
            state.content = value
        },
        updateWindow(state, value) {
            state.window = value
        }
    },
    actions: {
        SET_CONNECTIONS: async (context) => {
          let data = fetch ('http://localhost:8000/connections')
          let resp = data.then(response => { return response.json() })
          resp.then(connections => {context.commit('SET_CONNECTIONS', connections)})
        },
        SET_REQUESTS: async (context) => {
          let data = fetch ('http://localhost:8000/requests')
          let resp = data.then(response => { return response.json() })
          resp.then(connections => { context.commit('SET_REQUESTS', connections)})
        },
        SET_CREDENTIALS: async (context) => {
          let data = fetch ('http://localhost:8000/credentials')
          let resp = data.then(response => { return response.json() })
          resp.then(connections => {context.commit('SET_CREDENTIALS', connections)})
        },
        SET_LOCALS: async (context) => {
          let data = fetch ('http://localhost:8000/connections?geoip=1')
          let resp = data.then(response => { return response.json() })
          resp.then(connections => {context.commit('SET_LOCALS', connections)})
        },
        updateActive(context, value) {
            context.commit('updateActive', value)
        },
        updateContent(context, value) {
            context.commit('updateContent', value)
        },
        updateWindow(context, value) {
            context.commit('updateWindow', value)
        }
    }
});
