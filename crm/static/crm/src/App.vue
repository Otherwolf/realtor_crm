<template>
  <v-app id="app">
    <v-progress-linear
      style="z-index: 10000"
      v-if="isLoading"
      :active="isLoading"
      :indeterminate="isLoading"
      fixed
      color="blue accent-4"
    />
    <fc-menu/>
    <router-view/>
    <alerts/>
  </v-app>
</template>

<script>
import Menu from '@/components/base/Menu'
import Alert from '@/components/base/Alert'
import {mapGetters} from 'vuex'

export default {
  name: 'App',
  components: {
    'fc-menu': Menu,
    'alerts': Alert
  },
  computed: {
    ...mapGetters('Page', {isLoading: 'isLoading'})
  }
}
</script>

<style>
#app {
  width: 100vw;
  min-height: 100vh;
}

body {
  font-size: 0.9em;
  overflow: hidden; /* Hide scrollbars */
}

body::-webkit-scrollbar {
  display: none;
}

::-webkit-scrollbar-track {
  border-radius: 4px;
}

::-webkit-scrollbar {
  width: 1px;
}

::-webkit-scrollbar-thumb {
  border-radius: 4px;
  background: #f0f2f5;
}

:hover::-webkit-scrollbar-thumb {
  background: #6a7d9b;
}

.main-content {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

.outer {
  display: flex;
  height: 100%;
  flex-direction: row;
}

.block {
  height: 100%;
}

.block-1 {
  width: 25%;
}

.block-3 {
  width: 50%;
}

.block-2 {
  flex: 1; /* adjust automatically */
  min-width: 0; /* allow flexing beyond auto width */
  overflow: hidden; /* hide overflow on small width */
}

.slider {
  line-height: 100%;
  width: 5px;
  background-color: #c2c2c2;
  border: none;
  cursor: col-resize;
  user-select: none; /* disable selection */
  text-align: center;
}

.v-data-table__selected,
.v-list-item:hover {
  background-color: #f0f7ff !important;
}

.v-data-table__selected:hover {
  background-color: #dfe9f3 !important;
}

img {
  object-fit: cover;
}

.bckg {
  background: rgb(243, 242, 242);
  background: linear-gradient(156deg, rgb(241, 240, 240) 0%, rgb(255, 255, 255) 100%);
  width: 96vw;
}

.v-expansion-panel:before {
  box-shadow: none !important;
}

.body-container {
  max-width: 100%;
  overflow-x: hidden !important;
}
</style>
