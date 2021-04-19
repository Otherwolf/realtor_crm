<template>
  <v-navigation-drawer style="z-index: 1000" permanent expand-on-hover color="secondary">
    <v-list>
      <v-list-item class="px-2">
        <v-list-item-avatar>
          <v-img
            src="https://png.pngtree.com/template/20191014/ourmid/pngtree-home-or-house-roof-logo-design-template-with-water-wave-image_317799.jpg"></v-img>
        </v-list-item-avatar>
      </v-list-item>
      <v-list-item link to="/profile">
        <v-list-item-content>
          <v-list-item-title class="title">
            {{ username || '¯\\_(ツ)_/¯' }}
          </v-list-item-title>
          <v-list-item-subtitle class="primary--text">{{ user.email }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-list nav dense>
      <v-list-item link to="/index/lots">
        <v-list-item-icon>
          <v-icon color="primary">{{ icons.mdiFloorPlan }}</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Лоты</v-list-item-title>
      </v-list-item>
      <v-list-item link to="/index/complexes">
        <v-list-item-icon>
          <v-icon color="primary">{{ icons.mdiDomain }}</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Комплексы</v-list-item-title>
      </v-list-item>
    </v-list>
    <template v-slot:append>
      <div class="pa-2">
        <v-list nav dense>
          <v-list-item link href="/admin" v-if="user && user.is_superuser" target="_blank">
            <v-list-item-icon>
              <v-icon color="primary">{{ icons.mdiCogs }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Админ-панель</v-list-item-title>
          </v-list-item>
          <v-list-item link href="/logout">
            <v-list-item-icon>
              <v-icon color="primary">{{ icons.mdiLogoutVariant }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Выход</v-list-item-title>
          </v-list-item>
        </v-list>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import {mapGetters} from 'vuex'
import {mdiAccountHardHat, mdiCogs, mdiDomain, mdiFloorPlan, mdiLogoutVariant} from '@mdi/js'

export default {
  name: 'Menu',
  data() {
    return {
      icons: {
        mdiLogoutVariant,
        mdiCogs,
        mdiAccountHardHat,
        mdiDomain,
        mdiFloorPlan
      }
    }
  },
  computed: {
    ...mapGetters('User', {user: 'user'}),
    ...mapGetters('User', {username: 'getFullName'})
  }
}
</script>

<style scoped>
.v-navigation-drawer {
  position: fixed;
  height: 100vh;
  min-width: 61px !important;
}

</style>
