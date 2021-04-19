<template>
  <v-container>
    <v-app-bar app dense fixed color="secondary" style="margin-left: 61px">
      <v-row class="fill-height" style="overflow: hidden">
        <v-col cols="12" md="1" sm="1">
          <v-select
            dense
            v-model="data.priceFor"
            append-icon=""
            :items="itemsPrice"
            label="Цена"
          ></v-select>
        </v-col>
        <v-col cols="12" md="2" sm="3">
          <v-row>
            <v-col cols="10" md="6" sm="6" style="padding-right: 0">
              <vuetify-money
                dense
                class="centered-input right-border"
                :placeholder="'0'"
                v-model="data.price__lt"
                :label="'стоимость'"
                background-color="transparent"
                :options="optionsPrices"
              />
            </v-col>
            <v-col cols="10" md="6" sm="6" style="padding-left: 0">
              <vuetify-money
                dense
                class="centered-input"
                v-model="data.price__gt"
                :placeholder="'10 000 000'"
                background-color="transparent"
                :options="optionsPrices"
              />
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="12" md="1" sm="2">
          <v-row>
            <v-col cols="10" md="6" sm="6" style="padding-right: 0">
              <v-text-field
                v-model.number="data.s__lt"
                class="centered-input right-border"
                dense
                maxlength="4"
                placeholder="5"
                label="м²">
              </v-text-field>
            </v-col>
            <v-col cols="10" md="6" sm="6" style="padding-left: 0">
              <v-text-field
                v-model.number="data.s__gt"
                dense
                maxlength="4"
                class="centered-input"
                placeholder="1 300">
              </v-text-field>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="12" md="1" sm="2">
          <v-row>
            <v-col cols="10" md="6" sm="6" style="padding-right: 0">
              <v-text-field
                v-model.number="data.floor__lt"
                class="centered-input right-border"
                dense
                maxlength="3"
                placeholder="-2"
                label="этаж">
              </v-text-field>
            </v-col>
            <v-col cols="10" md="6" sm="6" style="padding-left: 0">
              <v-text-field
                dense
                maxlength="3"
                v-model.number="data.floor__gt"
                placeholder="95"
                class="centered-input">
              </v-text-field>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="12" md="1" sm="2">
          <v-select
            dense
            multiple
            item-text="text"
            item-value="value"
            v-model="data.bedroom"
            append-icon=""
            :items="itemsBedroom"
            label="cпальни"
          >
            <template v-slot:item="{item}">
              {{ item.text }}
            </template>
          </v-select>
        </v-col>
        <v-col cols="12" md="3" sm="3">
          <v-radio-group v-model="data.selectedType" row>
            <v-radio
              dense
              value="new"
              label="первичка"
              :on-icon="icons.mdiCheckboxMarked"
              :off-icon="icons.mdiCheckboxBlankOutline">
            </v-radio>
            <v-radio
              value="old"
              dense
              label="вторичка"
              :on-icon="icons.mdiCheckboxMarked"
              :off-icon="icons.mdiCheckboxBlankOutline"
            ></v-radio>
          </v-radio-group>
        </v-col>
        <v-col cols="12" md="3" sm="3" style="padding: 11px" align="end">
          <v-btn elevation="0" rounded color="primary" @click="filter" small>Подобрать</v-btn>
        </v-col>
      </v-row>
    </v-app-bar>
  </v-container>
</template>

<script>
import {mdiCheckboxBlankOutline, mdiCheckboxMarked, mdiMenuDown} from '@mdi/js'

export default {
  name: 'Header',
  data() {
    return {
      icons: {
        mdiMenuDown,
        mdiCheckboxMarked,
        mdiCheckboxBlankOutline
      },
      itemsPrice: ['лот', 'м²'],
      itemsBedroom: [
        {text: 'студия', value: 'студия'},
        {text: '1', value: 'с 1-ой спальней'},
        {text: '2', value: 'с 2-мя спальнями'},
        {text: '3', value: 'с 3-мя спальнями'},
        {text: '4+', value: 'с 4-ой спальней'}
      ],
      optionsPrices: {
        locale: 'ru-RU',
        prefix: '',
        suffix: '',
        length: 11,
        precision: 0
      },
      data: {
        priceFor: 'лот',
        price__lt: 0,
        price__gt: null,
        s__lt: 0,
        s__gt: null,
        floor__lt: -2,
        floor__gt: null,
        bedroom: [],
        selectedType: null
      }
    }
  },
  methods: {
    formatAsCurrency(value, dec) {
      dec = dec || 0
      if (value === null) {
        return 0
      }
      return '' + value.toFixed(dec).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,')
    },
    filter() {
      this.$store.dispatch('Page/setFilter', this.data, {root: true})
    }
  }
}
</script>

<style scoped>
.centered-input >>> input {
  text-align: center
}

.col,
.col-12 {
  padding: 15px 9px;
}

.v-input__control input {
  font-size: 0.8em;
}

.right-border {
  height: 25px;
  border-right: 1px solid grey;
}
</style>
