<template>
  <div style="height: 93vh; overflow: scroll" class="body-container">
    <v-row v-if="lot">
      <v-col md="12" sm="12" cols="12">
        <v-card min-height="70" class="pa-3">
          <h3> {{ lot.__str__ }} </h3>
          <br>
          <span class="grey--text float-right"
                v-if="lot.complex && lot.complex.developer"
          >
            <strong> {{ lot.complex.developer.name }} </strong>
          </span>
          <p>
            <span class="primary--text" v-if="lot.complex">
              <strong> {{ lot.complex.near_metro }}, </strong> {{ lot.complex.address }}
            </span><br>
            <span class="primary--text"><strong> {{ lot.lease }} </strong></span>
          </p>
        </v-card>
        <v-card class="pa-1" outlined color="transparent" v-if="images && images.length">
          <v-carousel
            :show-arrows="images.length > 1"
            hide-delimiters
            v-model="img"
            :next-icon="icons.mdiMenuRight"
            :prev-icon="icons.mdiMenuLeft"
            :delimiter-icon="icons.mdiCircleOutline"
            cycle
            style="width: auto; margin: auto"
            show-arrows-on-hover
            height="350px">
            <v-carousel-item v-for="(image) in images" :key="image.id">
              <v-img :src="image.get_url" contain height="350"/>
            </v-carousel-item>
          </v-carousel>
        </v-card>
        <v-card
          color="transparent"
          class="pa-1"
          outlined
          v-if="lot.links && lot.links.length"
        >
          <v-chip
            class="ma-2"
            color="primary"
            outlined
            v-for="(link, i) in lot.links"
            :key="i"
            :href="link.link"
            target="_blank"
          >
            {{ link.name }}
          </v-chip>
        </v-card>
        <v-expansion-panels multiple>
          <v-expansion-panel
            v-if="lot.contacts && lot.contacts.length"
            style="background-color: transparent !important;"
          >
            <v-expansion-panel-header :expand-icon="icons.mdiChevronDown">
              <h5 class="primary--text text-right">Контакты</h5>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card
                color="transparent"
                class="pa-1"
                outlined
                :key="contact.id"
                v-for="(contact) in lot.contacts"
                v-if="lot.contacts && lot.contacts.length"
              >
                <h5 class="primary--text">{{ contact.name }}</h5>
                <a :href="`tel:${contact.phone}`" v-if="contact.phone">{{ contact.phone }}<br></a>
                <a :href="`mailto:${contact.email}`" v-if="contact.email">{{ contact.email }}</a>
                <p class="grey--text" v-if="contact.note">{{ contact.note }}</p>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel v-if="lot.files && lot.files.length" style="background-color: transparent !important;">
            <v-expansion-panel-header :expand-icon="icons.mdiChevronDown">
              <h5 class="primary--text text-right">Презентации и документы</h5>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card
                color="transparent"
                class="pa-1"
                outlined
                v-for="(type, i) in new Set(lot.files.map(obj => obj.type))"
                :key="i"
              >
                <h4 class="primary--text">{{ type }}</h4>
                <v-card
                  color="transparent"
                  class="pa-1"
                  outlined
                  v-for="(file, index) in lot.files.filter(obj => obj.type === type)"
                  :key="index"
                >
                  <h5 v-if="file.name">{{ file.name }}</h5>
                  <a :href="file.get_url">
                    <span>{{ file.filename }}</span>
                  </a>
                  <p class="grey--text">
                    <span>{{ file.get_created_at }}</span> | <span>{{ file.get_size }}</span>
                  </p>
                </v-card>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <v-card color="transparent">
          <v-expansion-panels multiple>
            <v-expansion-panel>
              <v-expansion-panel-header :expand-icon="icons.mdiChevronDown">
                <h5 class="primary--text">Лот</h5>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-simple-table>
                  <template v-slot:default>
                    <tbody>
                    <tr v-if="lot.n_on_price">
                      <td>№ по прайсу</td>
                      <td>{{ lot.n_on_price }}</td>
                    </tr>
                    <tr v-if="lot.type_object">
                      <td>Тип объекта</td>
                      <td>{{ lot.type_object.name }}</td>
                    </tr>
                    <tr v-if="lot.corp">
                      <td>Корпус</td>
                      <td>{{ lot.corp.name }}</td>
                    </tr>
                    <tr v-if="lot.floor">
                      <td>Этаж</td>
                      <td>{{ lot.floor }}</td>
                    </tr>
                    <tr v-if="lot.s">
                      <td>Площадь</td>
                      <td>{{ lot.s }}м²</td>
                    </tr>
                    <tr v-if="lot.trim">
                      <td>Отделка</td>
                      <td>{{ lot.trim }}</td>
                    </tr>
                    <tr v-if="lot.view_from_windows">
                      <td>Вид из окон</td>
                      <td>{{ lot.view_from_windows }}</td>
                    </tr>
                    <tr v-if="lot.options">
                      <td>Опции</td>
                      <td>{{ lot.options }}</td>
                    </tr>
                    <tr v-if="lot.reward">
                      <td>Вознаграждение</td>
                      <td>{{ lot.reward }}</td>
                    </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel>
              <v-expansion-panel-header :expand-icon="icons.mdiChevronDown">
                <h5 class="primary--text">Цена</h5>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-simple-table>
                  <template v-slot:default>
                    <tbody>
                    <tr v-if="lot.price">
                      <td>Цена в Руб.</td>
                      <td>{{ humanized_sum(lot.price) }}</td>
                    </tr>
                    <tr v-if="lot.price_per_m">
                      <td>Руб. за м²</td>
                      <td>{{ humanized_sum(lot.price_per_m) }}</td>
                    </tr>
                    <tr v-if="lot.currency">
                      <td>Цена в $</td>
                      <td>{{ humanized_sum(lot.currency) }}</td>
                    </tr>
                    <tr v-if="lot.currency_per_m">
                      <td>$ за м²</td>
                      <td>{{ humanized_sum(lot.currency_per_m) }}</td>
                    </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
import {mdiChevronDown, mdiCircleOutline, mdiMenuLeft, mdiMenuRight} from '@mdi/js'

export default {
  name: 'MainLot',
  data() {
    return {
      img: 0,
      icons: {
        mdiMenuLeft,
        mdiMenuRight,
        mdiCircleOutline,
        mdiChevronDown
      }
    }
  },
  computed: {
    ...mapGetters('Page', {lot: 'getMain'}),
    images() {
      if (this.lot && this.lot.images) {
        let arr = [{get_url: this.lot.url_plan, id: 0}].concat(this.lot.images).concat(this.lot.complex.images)
        return arr
      }
      return []
    }
  },
  methods: {
    humanized_sum(sum) {
      return parseInt(sum).toLocaleString()
    }
  }
}
</script>

<style scoped>
.v-sheet {
  box-shadow: none;
}
</style>
