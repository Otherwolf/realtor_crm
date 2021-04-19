<template>
  <div style="height: 95vh; overflow: scroll" ref="subscroll">
    <v-data-table
      :headers="headers"
      :items="developers"
      hide-default-footer
      item-key="id"
      disable-pagination
      disable-sort
      @click:row="selectItems($event.id), selected = [$event]"
      fixed-header
      v-model="selected"
      :items-per-page="developers.length"
      class="elevation-0"
    >
      <template v-slot:item.name="{ item }">
        <a href="#" @click.prevent="$emit('selectItem', 'developer', item.id)">{{ item.name }}</a>
      </template>
      <template v-slot:item.count_complexes="{ item }">
        <a href="#" @click.prevent="$emit('selectGroup')" class="float-right">{{ item.count_complexes}} жк</a>
      </template>
    </v-data-table>
    <div>
      <mugen-scroll
        :handler="fetchData"
        :should-handle="!loading"
        scrollContainer="subscroll"
        v-if="!isFinished"
        class="text-center">
        Загрузка...
      </mugen-scroll>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
import MugenScroll from 'vue-mugen-scroll'

export default {
  name: 'SubDevelopers',
  components: {
    'mugen-scroll': MugenScroll
  },
  data () {
    return {
      selected: [],
      loading: false,
      counter: 30,
      headers: [
        { text: 'Имя', value: 'name' },
        { text: 'Число ЖК', value: 'count_complexes' }
      ]
    }
  },
  computed: {
    ...mapGetters('Page', {developers: 'getSub'}),
    ...mapGetters('Page', {isFinished: 'isSubFinished'})
  },
  created () {
    this.fetchData()
  },
  methods: {
    selectItems (id) {
      const itemsForRemove = document.querySelectorAll('.v-data-table__selected')
      itemsForRemove.forEach(item => {
        item.classList.remove('v-data-table__selected')
      })
      const items = document.querySelectorAll(`.developer-${id}`)
      items.forEach(item => {
        item.closest('tr').classList.add('v-data-table__selected')
      })
      items[0].scrollIntoView({
        behavior: 'smooth'
      })
    },
    fetchData () {
      this.loading = true
      this.$store.dispatch('Page/subload', {
        page: this.$route.name
      }, {
        root: true
      })
      setTimeout(() => {
        this.counter = this.developers.length
        this.loading = false
      }, 10)
    }
  }
}
</script>
