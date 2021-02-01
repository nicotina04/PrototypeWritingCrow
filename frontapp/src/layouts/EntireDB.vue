<template>
  <q-page class="flex-center">
    <div>
    </div>
    <q-table
      ref="table"
      title="로그 조회"
      :data="goodscan"
      :columns="columns"
      :filter="filter"
      :filter-method='filterData'
      row-key="date"
      :pagination.sync="initialPagination"
      :loading="loading"
      virtual-scroll
      :rows-per-page-options="[0]"
      hide-pagination
    >
    <template v-slot:top-row>
      <q-tr>
        <q-td>
        </q-td>
        <q-td>
          <q-input outlined v-model="filter.id" label="바코드 검색" dense></q-input>
        </q-td>
        <q-td align='center'>
          <q-select
            clearable
            :options="categoryoptions"
            label="검색 분야 선택"
            emit-value
            map-options
            v-model="filter.category"
          >
          </q-select>
        </q-td>
          <q-td>
          <q-input outlined v-model="filter.title" label="제목 검색" dense></q-input>
        </q-td>
        <q-td>
          <q-input outlined v-model="filter.author" label="저자 검색" dense></q-input>
        </q-td>
        <q-td>
          <q-input outlined v-model="filter.publisher" label="출판사 검색" dense></q-input>
        </q-td>
        <q-td>
        </q-td>
      </q-tr>
    </template>
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
import isbn from 'assets/isbn.json'
import goodscan from 'assets/log.json'

Object.freeze(isbn)
Object.freeze(goodscan)
Object.freeze(bookid)

export default {
  name: 'EntireDB',
  data () {
    return {
      leftDrawerOpen: false,
      goodscan,
      bookid,
      categoryoptions: Object.keys(bookid).filter((item) => {
        return Number(item) < 300
      }).map((e) => {
        return {
          label: bookid[e],
          value: e
        }
      }),
      filteredpages: 0,
      loading: false,
      filter: {
        id: '',
        category: null,
        title: '',
        author: '',
        publisher: ''
      },
      initialPagination: {
        sortBy: 'date',
        descending: false,
        page: 1,
        rowsPerPage: 10
      },
      columns: [
        {
          align: 'left',
          name: 'date',
          label: '일시',
          field: row => row.date
        },
        {
          align: 'left',
          name: 'id',
          label: '일련번호',
          field: row => row.id
        },
        {
          align: 'center',
          name: 'category',
          label: '분야',
          field: row => row.id,
          format: (val) => `${isbn[val] !== undefined ? bookid[isbn[val].categoryId] ? bookid[isbn[val].categoryId] : '카테고리 없음' : '카테고리 없음'}`
        },
        {
          align: 'left',
          name: 'title',
          label: '제목',
          field: row => row.id,
          format: (val) => `${isbn[val] !== undefined ? isbn[val].title : '제목 정보 없음'}`
        },
        {
          align: 'left',
          name: 'author',
          label: '저자',
          field: row => row.id,
          format: (val) => `${isbn[val] !== undefined ? isbn[val].author : '저자 정보 없음'}`
        },
        {
          align: 'left',
          name: 'publisher',
          label: '출판사',
          field: row => row.id,
          format: (val) => `${isbn[val] !== undefined ? isbn[val].publisher : '출판사 정보 없음'}`
        }
      ]
    }
  },
  computed: {
    pagesNumber () {
      return Math.ceil(this.filteredpages / this.initialPagination.rowsPerPage)
    }
  },
  methods: {
    filterData (rows, terms, cols, getCellValue) {
      for (const term in terms) {
        rows = rows.filter((row) => {
          if (term === 'id') {
            return row.id.toLowerCase().indexOf((this.filter[term] + '').toLowerCase()) !== -1
          } else if (term === 'category') {
            if (this.filter.category === null) {
              return true
            } else if (isbn[row.id] === undefined) {
              return false
            } else {
              const tmp = isbn[row.id].categoryId
              const cat = this.filter.category
              if (cat === '100') {
                return Number(tmp) >= 100 && Number(tmp) < 200
              } else if (cat === '200') {
                return Number(tmp) >= 200 && Number(tmp) < 300
              }
              return cat === tmp
            }
          } else {
            const word = isbn[row.id]
            if (word === undefined) {
              return false
            }
            return word[term].toLowerCase().indexOf((this.filter[term] + '').toLowerCase()) !== -1
          }
        })
      }
      this.filteredpages = rows.length
      return rows
    }
  }
}
</script>
