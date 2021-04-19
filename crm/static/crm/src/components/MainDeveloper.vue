<template>
  <div style="height: 93vh; overflow: scroll" class="body-container">
    <v-row>
      <v-col md="12" sm="12" cols="12">
        <v-card class="pa-3">
          <h3>Застройщик {{ developer.name }}</h3> <br>
          <span class="grey--text">Дата основания: {{ developer.created_at }}</span>
        </v-card>
        <v-spacer/>
        <v-card v-if="percentage_objects_under_construction" class="pa-1">
          <span>
            <v-progress-circular
              :rotate="180"
              :size="70"
              :width="10"
              :value="percentage_objects_under_construction"
              color="primary"
            >
              <span class="black--text">{{ developer.objects_under_construction }}</span>
            </v-progress-circular>
            <p class="grey--text circular-label">На стадии строительства</p>
          </span>
          <span class="float-right">
            <v-progress-circular
              :rotate="180"
              :size="70"
              :width="10"
              :value="100 - percentage_objects_under_construction"
              color="blue"
            >
              <span class="black--text">{{ developer.objects_delivered }}</span>
            </v-progress-circular>
            <p class="grey--text circular-label">Построено объектов</p>
          </span>
        </v-card>
        <v-card
          class="pa-1"
          outlined
          color="transparent"
          v-if="developer.images && developer.images.length"
        >
          <v-carousel
            :show-arrows="developer.images.length > 1"
            hide-delimiters
            v-model="img"
            :next-icon="icons.mdiMenuRight"
            :prev-icon="icons.mdiMenuLeft"
            :delimiter-icon="icons.mdiCircleOutline"
            cycle
            show-arrows-on-hover
            style="width: auto; margin: auto"
            height="100"
          >
            <v-carousel-item
              v-for="(image) in developer.images"
              :key="image.id"
            >
              <v-img :src="image.get_url" contain height="100"></v-img>
            </v-carousel-item>
          </v-carousel>
        </v-card>
        <v-card color="transparent" class="pa-1" outlined v-if="developer.links && developer.links.length">
          <v-chip
            class="ma-2"
            color="primary"
            outlined
            v-for="(link, i) in developer.links"
            :key="i"
            :href="'http://' + link.link"
            target="_blank"
          >
            {{ link.name }}
          </v-chip>
        </v-card>
        <v-expansion-panels multiple>
          <v-expansion-panel
            v-if="developer.contacts && developer.contacts.length"
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
                v-for="(contact) in developer.contacts"
                v-if="developer.contacts && developer.contacts.length"
              >
                <h5 class="primary--text">{{ contact.name }}</h5>
                <a :href="`tel:${contact.phone}`" class="grey--text" v-if="contact.phone">{{ contact.phone }}<br></a>
                <a :href="`mailto:${contact.email}`" class="grey--text" v-if="contact.email">{{ contact.email }}</a>
                <p v-if="contact.note">{{ contact.note }}</p>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <v-card color="transparent">
          <v-expansion-panels v-model="panels" multiple>
            <v-expansion-panel v-show="developer.description">
              <v-expansion-panel-header :expand-icon="icons.mdiChevronDown">
                <h5 class="primary--text">Информация о застройщике</h5>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <p>{{ developer.description }}</p>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel v-if="developer.complexes" v-model="panels">
              <v-expansion-panel-header :expand-icon="icons.mdiChevronDown">
                <h5 class="primary--text">Объекты</h5>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-data-table
                  dense
                  :headers="headers"
                  :items="developer.complexes"
                  disable-sort
                  hide-default-footer
                  disable-pagination
                  :items-per-page="developer.complexes.length"
                  class="elevation-0"
                >
                </v-data-table>
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
  name: 'MainDeveloper',
  data() {
    return {
      panels: [1],
      headers: [
        {text: 'Имя', value: 'name'},
        {text: 'В продаже', value: 'count_lots_in_sale'},
        {text: 'Сдача', value: 'end_of_construction'}
      ],
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
    ...mapGetters('Page', {developer: 'getMain'}),
    percentage_objects_under_construction() {
      if (this.developer.objects_under_construction !== undefined) {
        const sum = this.developer.objects_under_construction + this.developer.objects_delivered
        return this.developer.objects_under_construction / sum * 100
      } else {
        return 0
      }
    }
  }
}
</script>

<style scoped>
.circular-label {
  width: 110px;
  display: inline-block;
  position: relative;
  top: 10px;
}

.v-sheet {
  box-shadow: none;
}
</style>
