<template>
  <div style="height: 95vh; overflow: scroll" ref="subscroll">
    <v-data-table
      :headers="headers"
      :items="complexes"
      hide-default-footer
      item-key="id"
      v-model="selected"
      @click:row="selectItems($event.id), selected = [$event]"
      disable-pagination
      disable-sort
      fixed-header
      :items-per-page="complexes.length"
      class="elevation-0"
    >
      <template v-slot:item.name="{ item }">
        <a href="#" @click.prevent="$emit('selectItem', 'complex', item.id)">{{ item.name }}</a>
      </template>
      <template v-slot:item.count_lots_in_sale="{ item }">
        <a href="#" @click.prevent="$emit('selectGroup')" class="float-right">{{ item.count_lots_in_sale }} лотов</a>
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
  name: 'SubComplexes',
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
        { text: 'Число лотов', value: 'count_lots_in_sale' }
      ]
    }
  },
  computed: {
    ...mapGetters('Page', {complexes: 'getSub'}),
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
      const items = document.querySelectorAll(`.complex-${id}`)
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
        this.counter = this.complexes.length
        this.loading = false
      }, 10)
    }
  }
}
</script>
