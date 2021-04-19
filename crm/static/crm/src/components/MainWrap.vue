<template>
  <div style="padding-top: 0">
    <v-row dense>
      <v-col cols="12" md="1" sm="12">
        <a href="#" @click.prevent="$emit('selectGroup'), removeSelectedItems()">
          <v-icon color="primary">{{ icons.mdiArrowLeft }}</v-icon>
        </a>
      </v-col>
      <v-col cols="12" md="3" sm="12">
        <a :href="`/admin/crm/${type}/${id}/change/`" target="_blank"
           v-if="id !== null && (user.is_superuser || user.is_staff)">
          <strong>Редактировать</strong>
        </a>
      </v-col>
      <v-col cols="12" md="8" sm="12" align="end" v-if="id !== null">
        <span v-if="updated_by">
          {{ updated_by }}
        </span>
      </v-col>
    </v-row>
    <complex v-if="type === 'complex'"/>
    <developer v-else-if="type === 'developer'"/>
    <lot v-else/>
  </div>
</template>

<script>
import {mdiArrowLeft} from '@mdi/js'
import {mapGetters} from 'vuex'
import MainDeveloper from './MainDeveloper'
import MainLot from './MainLot'
import MainComplex from './MainComplex'

export default {
  name: 'MainWrap',
  props: ['id', 'type'],
  components: {
    'complex': MainComplex,
    'developer': MainDeveloper,
    'lot': MainLot
  },
  data() {
    return {
      icons: {
        mdiArrowLeft
      }
    }
  },
  computed: {
    ...mapGetters('Page', {obj: 'getMain'}),
    ...mapGetters('User', {user: 'user'}),
    updated_by() {
      const user = this.obj.updated_by
      const time = this.obj.updated_at
      if (!user || !time) return ''
      const localTime = new Date(time).toLocaleString('ru', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
      })
      return `${user.first_name} ${user.last_name},  ${localTime}`
    }
  },
  created() {
    if (this.id !== null) {
      this.$store.dispatch('Page/loadMain',
        {id: this.id, type: this.type},
        {root: true})
    }
  },
  methods: {
    removeSelectedItems() {
      const items = document.querySelectorAll('.v-data-table__selected')
      items.forEach(item => {
        item.classList.remove('v-data-table__selected')
      })
    }
  }
}
</script>
