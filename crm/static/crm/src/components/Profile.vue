<template>
  <v-container>
    <!--    <v-expansion-panels v-model="panel" multiple>-->
    <!--      <v-expansion-panel class="text-center">-->
    <!--        <v-expansion-panel-header color="accent" class="text-center" :expand-icon="icons.mdiChevronDown">-->
    <!--          <h4 class="primary&#45;&#45;text">Персональные данные</h4>-->
    <!--        </v-expansion-panel-header>-->
    <!--        <v-expansion-panel-content>-->
    <!--          пароль и тд-->
    <!--        </v-expansion-panel-content>-->
    <!--      </v-expansion-panel>-->
    <!--    </v-expansion-panels>-->
  </v-container>
</template>

<script>
import {mdiChevronDown, mdiClose} from '@mdi/js'

export default {
  name: 'Profile',
  data() {
    return {
      panel: [0],
      icons: {
        mdiClose,
        mdiChevronDown
      }
    }
  }
}
</script>
