<template>
  <v-container style="margin-left: 61px; position: fixed">
    <v-row>
      <v-col cols="12" sm="12" md="12">
        <fc-header/>
      </v-col>
    </v-row>
    <v-row class="fill-height bckg">
      <!--    контент-->
      <v-col style="padding: 0" class="main-content" cols="12" sm="12" md="12">
        <div class="outer">
          <div class="block block-1" ref="block1" v-show="navigation.shown">
            <router-view @selectItem="onSelectSubItem" @selectGroup="onSelectGroup" name="sub"/>
          </div>
          <div class="slider" ref="slider1" v-show="navigation.shown"/>
          <div class="block block-2" ref="block2" v-show="navigationC.shown">
            <router-view name="main" @selectItem="onSelectSubItem"/>
          </div>
          <div class="slider" ref="slider2" v-show="!navigation.shown && navigationR.shown"/>
          <div class="block block-2" ref="block3" v-show="navigationR.shown">
            <main-wrap
              :key="navigationR.type + navigationR.id"
              v-if="navigationR.id"
              @selectGroup="onSelectGroup"
              :id="navigationR.id"
              :type="navigationR.type"
            />
          </div>
          <!--      Конец контента-->
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Header from './base/Header'
import {mdiPlusBoxOutline} from '@mdi/js'
import MainWrap from './MainWrap'

export default {
  name: 'Index',
  components: {
    'fc-header': Header,
    'main-wrap': MainWrap
  },
  data() {
    return {
      icons: {mdiPlusBoxOutline},
      dataL: Array(10).fill(Math.floor(Math.random() * Math.floor(10000))),
      navigation: {
        shown: true
      },
      navigationC: {
        hasToggled: false,
        shown: true
      },
      navigationR: {
        id: null,
        type: null,
        shown: false
      }
    }
  },
  beforeRouteUpdate(to, from, next) {
    this.setBlocksVisibility()
    next()
  },
  mounted() {
    this.setEvents()
  },
  methods: {
    toggleCLassOnBlock() {
      let block = this.$refs.block2
      if (['newbuildinglot', 'oldbuildinglot'].includes(this.navigationR.type)) {
        block.classList.toggle('block-3')
      } else {
        block.classList.toggle('block-1')
      }
      block.classList.toggle('block-2')
    },
    setBlocksVisibility(b1 = true, b2 = true, b3 = false) {
      this.navigation.shown = b1
      this.navigationR.shown = b3
      this.navigationC.shown = b2
      if (this.navigationC.hasToggled && !b3) {
        this.toggleCLassOnBlock()
        this.navigationC.hasToggled = false
        this.setEvents()
      } else if (!this.navigationC.hasToggled && b3) {
        this.toggleCLassOnBlock()
        const block = this.$refs.block2
        const slide = this.$refs.slider2
        this.navigationC.hasToggled = true
        this.setEvents(block, slide)
      }
    },
    setEvents(el = null, slide = null) {
      let block = el || this.$refs.block1
      let slider = slide || this.$refs.slider1

      slider.onmousedown = function dragMouseDown(e) {
        let dragX = e.clientX
        document.onmousemove = function onMouseMove(e) {
          block.style.width = block.offsetWidth + e.clientX - dragX + 'px'
          dragX = e.clientX
        }
        // remove mouse-move listener on mouse-up
        document.onmouseup = () => {
          document.onmousemove = document.onmouseup = null
        }
      }
    },
    onSelectGroup(id = null) {
      this.setBlocksVisibility()
    },
    onSelectSubItem(mainPage = null, id = null, statuses = []) {
      this.navigationR.id = id
      this.navigationR.type = mainPage
      if (!statuses.length) {
        this.setBlocksVisibility(true, false, true)
      } else {
        this.setBlocksVisibility(...statuses)
      }
    }
  }
}
</script>

