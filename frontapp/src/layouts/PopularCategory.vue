<template>
  <q-page class='flex-center'>
    <q-banner inline-actions>
      분야별 스캔 횟수 조회
    </q-banner>
    <div class="q-pa-md q-gutter-sm">
      <q-btn flat color="primary" label="최근 24시간" @click="selectDay(1)"/>
      <q-btn flat color="primary" label="최근 7일" @click="selectDay(7)"/>
      <q-btn flat color="primary" label="최근 30일" @click="selectDay(30)"/>
      <q-btn flat color="primary" label="날짜 지정하기">
        <q-tooltip content-class="bg-accent">시작 날짜와 종료 날짜 선택</q-tooltip>
        <q-popup-proxy @before-show="updateProxy" transition-show="scale" transition-hide="scale">
          <q-date v-model="proxyDate" range>
            <div class="row items-center justify-end q-gutter-sm">
              <q-btn label="취소" color="primary" flat v-close-popup/>
              <q-btn label="확인" color="primary" flat @click="save()" v-close-popup />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-btn>
      <q-btn color="primary" label="기간 초기화" @click="resetDate()"/>
      <q-btn color="primary" label="검색" @click="calculateCatCount()"/>
      <div v-if="this.duration.from && this.duration.to">
        기간: {{this.duration.from.getFullYear() + ":" + (this.duration.from.getMonth() + 1) + ":" + this.duration.from.getDate()}} ~ {{this.duration.to.getFullYear() + ":" + (this.duration.to.getMonth() + 1) + ":" + this.duration.to.getDate()}}
      </div>
      <div v-else>
        기간 설정이 되지 않았습니다.
      </div>
      <q-select
        clearable
        :options="categoryoptions"
        label="검색 분야 선택"
        emit-value
        map-options
        v-model="category"
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

    resetDate () {
      this.duration = {}
      this.proxyDate = {}
      this.dateRange = {}
    },

    save () {
      this.dateRange = this.proxyDate
      this.duration.from = new Date(this.dateRange.from)
      this.duration.to = new Date((new Date(this.dateRange.to)).setHours(23, 59, 59))
    },

    selectDay (day) {
      this.proxyDate = {}
      var now = new Date()
      this.duration.from = new Date(now.getTime() - (day * 24 * 60 * 60 * 1000))
      this.duration.to = now
    },

    calculateCatCount () {
      this.scanCount = {}
      let filteredlog = goodscan

      if (this.category !== null) {
        filteredlog = filteredlog.filter((item) => {
          if (isbn[item.id] === undefined) {
            return false
          }

          const catId = parseInt(this.category)
          const tmp = parseInt(isbn[item.id].categoryId)

          if (catId === 100) {
            return tmp >= 100 && tmp < 200
          } else if (catId === 200) {
            return tmp >= 200 && tmp < 300
          } else {
            return tmp === catId
          }
        })
      }

      let l = 0
      let r = filteredlog.length - 1
      let idx

      if (this.duration.from !== undefined) {
        while (l <= r) {
          const m = parseInt(l + (r - l) / 2)

          if (new Date(filteredlog[m].date) >= this.duration.from) {
            idx = m
            r = m - 1
          } else {
            l = m + 1
          }
        }
      } else {
        idx = 0
      }

      if (idx !== undefined) {
        for (let i = idx; i < filteredlog.length; ++i) {
          const booklog = filteredlog[i]
          const idxisbn = booklog.id

          if (new Date(booklog.date) > this.duration.to) {
            break
          }

          // 인터파크에 등록되지 않은 도서는 카테고리를 일괄 '000'으로 처리
          if (isbn[idxisbn] === undefined) {
            if (this.scanCount['000'] === undefined) {
              this.scanCount['000'] = 1
            } else {
              ++this.scanCount['000']
            }
          } else {
            if (this.scanCount[isbn[idxisbn].categoryId] === undefined) {
              this.scanCount[isbn[idxisbn].categoryId] = 1
            } else {
              ++this.scanCount[isbn[idxisbn].categoryId]
            }
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
