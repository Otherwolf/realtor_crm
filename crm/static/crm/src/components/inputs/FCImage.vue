<template>
  <div>
    <v-btn fab small depressed color="transparent">
      <v-tooltip right>
        <template v-slot:activator="{ on, attrs }">
          <v-img :src="link" width="40" height="40" v-on="on">
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular indeterminate color="grey lighten-5"/>
              </v-row>
            </template>
          </v-img>
        </template>
        <v-img :src="link" width="250" height="auto">
          <template v-slot:placeholder>
            <v-row class="fill-height ma-0" align="center" justify="center">
              <v-progress-circular indeterminate color="grey lighten-5"/>
            </v-row>
          </template>
        </v-img>
      </v-tooltip>
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'FCImage',
  props: ['link']
}
</script>

