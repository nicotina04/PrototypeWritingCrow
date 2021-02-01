<template>
  <q-page class='flex-center'>
    <q-banner inline-actions>
      분야별 스캔 횟수 조회
    </q-banner>
    <div class="q-pa-md q-gutter-sm">
      <q-btn flat color="primary" label="최근 24시간" @click="selectDay(1); caculateScanCount()"/>
      <q-btn flat color="primary" label="최근 7일" @click="selectDay(7); caculateScanCount()"/>
      <q-btn flat color="primary" label="최근 30일" @click="selectDay(30); caculateScanCount()"/>
      <q-btn flat color="primary" label="날짜 지정하기">
        <q-tooltip content-class="bg-accent">시작 날짜와 종료 날짜 선택</q-tooltip>
        <q-popup-proxy @before-show="updateProxy" transition-show="scale" transition-hide="scale">
          <q-date v-model="proxyDate" range>
            <div class="row items-center justify-end q-gutter-sm">
              <q-btn label="취소" color="primary" flat v-close-popup />
              <q-btn label="확인" color="primary" flat @click="save(); caculateScanCount()" v-close-popup />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-btn>
      <q-select
        clearable
        :options="categoryoptions"
        label="검색 분야 선택"
        emit-value
        map-options
        v-model="category"
        @click="caculateScanCount()"
      >
      </q-select>
    </div>
    <br>
    <q-table
    ref="table"
    :data="tableData"
    :columns="columns"
    :pagination.sync="initialPagination"
    virtual-scroll
    :rows-per-page-options="[0]"
    hide-pagination
    >
    </q-table>
    <div class="row justify-center q-mt-md">
      <q-pagination
        v-model="initialPagination.page"
        color="grey-8"
        :max="pagesNumber"
        :input="true"
      />
    </div>
  </q-page>
</template>

<script>
import bookid from 'assets/interparkbookid.json'
import goodscan from 'assets/log.json'
import isbn from 'assets/isbn.json'

Object.freeze(goodscan)
Object.freeze(isbn)
Object.freeze(bookid)

export default {
  name: 'PopularCategory',
  data () {
    return {
      categoryoptions: Object.keys(bookid).filter((item) => {
        return Number(item) < 300
      }).map((e) => {
        return {
          label: bookid[e],
          value: e
        }
      }),
      category: null,
      scanCount: {},
      tableData: [],
      duration: {},
      dateRange: {},
      proxyDate: {},
      initialPagination: {
        descending: false,
        page: 1,
        rowsPerPage: 5
      },
      columns: [
        {
          name: 'category',
          label: '분야',
          align: 'left',
          field: row => row[0],
          format: (val) => `${isbn[val] !== '000' ? bookid[val] ? bookid[val] : '카테고리 없음' : '카테고리 없음'}`
        },
        {
          name: 'counted',
          label: '스캔 횟수',
          align: 'center',
          field: row => row[1]
        }
      ]
    }
  },
  computed: {
    pagesNumber () {
      return Math.ceil(this.tableData.length / this.initialPagination.rowsPerPage)
    }
  },
  methods: {
    updateProxy () {
      this.proxyDate = this.dateRange
    },

    save () {
      this.dateRange = this.proxyDate
      this.duration.from = new Date(this.dateRange.from)
      this.duration.to = new Date((new Date(this.dateRange.to)).setHours(23, 59, 59))
    },

    selectDay (day) {
      var now = new Date()
      this.duration.from = new Date(now.getTime() - (day * 24 * 60 * 60 * 1000))
      this.duration.to = now
    },

    caculateScanCount () {
      this.scanCount = {}
      let filteredlog = goodscan
      if (this.category !== null) {
        filteredlog = filteredlog.filter((item) => {
          if (isbn[item.id] === undefined) {
            return false
          }

          const tmp = Number(isbn[item.id].categoryId)

          if (this.category === '100') {
            return tmp >= 100 && tmp < 200
          } else if (this.category === '200') {
            return tmp >= 200 && tmp < 300
          } else {
            return tmp === Number(this.category)
          }
        })
      }
      let l = 0
      let r = filteredlog.length - 1
      let idx

      while (l <= r) {
        const m = parseInt(l + (r - l) / 2)

        if (new Date(filteredlog[m].date) >= this.duration.from) {
          idx = m
          r = m - 1
        } else {
          l = m + 1
        }
      }

      if (idx !== undefined) {
        for (let i = idx; i < filteredlog.length; ++i) {
          if (new Date(filteredlog[i].date) > this.duration.to) {
            break
          }

          if (this.scanCount[isbn[filteredlog[i].id].categoryId] === undefined) {
            this.scanCount[isbn[filteredlog[i].id].categoryId] = 1
          } else {
            ++this.scanCount[isbn[filteredlog[i].id].categoryId]
          }
        }
      }

      var resultArr = []

      for (const key in this.scanCount) {
        const tmp = []
        tmp.push(key)
        tmp.push(this.scanCount[key])
        resultArr.push(tmp)
      }

      resultArr.sort((a, b) => {
        return b[1] - a[1]
      })

      this.tableData = resultArr
    }
  }
}
</script>
