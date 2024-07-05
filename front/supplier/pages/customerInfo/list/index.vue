<!-- 顧客一覧画面 -->
<template>
  <div>
    <div class="title">
      <h1>顧客一覧</h1>
    </div>
    <div class="list-header">
      <div class="list-header-item clickable" @click="sortBy('name')">
        氏名 <span v-if="sortKey === 'name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
      </div>
      <div class="list-header-item">性別</div>
      <div class="list-header-item clickable" @click="sortBy('lastReservedDate')">
        最終来店日 <span v-if="sortKey === 'lastReservedDate'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
      </div>
      <div class="list-header-item clickable" @click="sortBy('nextReservedDate')">
        次の予約 <span v-if="sortKey === 'nextReservedDate'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
      </div>
    </div>
    <div class="list-body">
      <div class="list-content">
        <div v-for="customer in sortedCustomers" :key="customer.id" class="list-record">
          <a :href="`/customerInfo/detail/${customer.id}`" class="customer-link">
            <div class="list-info">
              <div class="list-item">{{ customer.name }}</div>
              <div class="list-item">{{ customer.gender }}</div>
              <div class="list-item">{{ customer.lastReservedDate | datetime2date }}<br>{{ customer.lastReservedSttime }}</div>
              <div class="list-item">{{ customer.nextReservedDate | datetime2date }}<br>{{ customer.nextReservedSttime }}</div>
            </div>
          </a>
        </div>
      </div>
    </div>
    <div class="buttons">
      <button class="edit-button" @click="returnIndex">戻る</button>
    </div>
  </div>
</template>

<script>
import common from '@/plugins/common'
export default {
  filters: {
    datetime2date(value) {
      if (!value) return '';
      const datetime = new Date(value);
      const year = datetime.getFullYear();
      const month = String(datetime.getMonth() + 1).padStart(2, '0');
      const day = String(datetime.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    datetime2hhmm(value) {
      if (!value) return '';
      const datetime = new Date(value);
      const hours = String(datetime.getHours()).padStart(2, '0');
      const minutes = String(datetime.getMinutes()).padStart(2, '0');
      return `${hours}:${minutes}`;
    },
    hhmmss2hhmm(value) {
      if (!value) return '';
      const [hours, minutes] = value.split(':');
      return `${hours}:${minutes}`;
    }
  },
  layout: 'supplier',
  data() {
    return {
      // 開発のためliffコメントアウト
      // this.$liffInit
      //   .then(() => {
      //     this.idToken = liff.getIDToken();
      //     // this.accessToken = liff.getAccessToken();
      //   })
      //   .catch((error) => {
      //     this.liffError = error
      //   })
      customerMst: [],
      sortKey: 'name', // デフォルトのソートキー
      sortOrder: 'asc' // デフォルトのソート順序
    }
  },
  computed: {
    sortedCustomers() {
      return [...this.customerMst].sort((a, b) => {
        let aValue = a[this.sortKey];
        let bValue = b[this.sortKey];
        
        // 日付型の場合、比較前に Date オブジェクトに変換
        if (this.sortKey === 'lastReservedDate' || this.sortKey === 'nextReservedDate') {
          aValue = aValue ? new Date(aValue) : new Date(0);
          bValue = bValue ? new Date(bValue) : new Date(0);
        }
        
        if (aValue < bValue) return this.sortOrder === 'asc' ? -1 : 1;
        if (aValue > bValue) return this.sortOrder === 'asc' ? 1 : -1;
        return 0;
      });
    }
  },
  mounted() {
    this.getCustomerMst()
  },
  methods:{
    async getCustomerMst(){
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetCustomerMst'
      const data = {withReserveInfo: 1}
      const res = await common.gateway_get(apiurl, data)
      this.customerMst = res
    },
    returnIndex(){
      this.$router.push(`/`)
    },
    sortBy(key) {
      if (this.sortKey === key) {
        // 同じキーでソートする場合は順序を反転
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        // 新しいキーでソートする場合は昇順から開始
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
    }
  },
}
</script>

<style>
.customer-link {
  display: flex;
  flex-grow: 1;
  text-decoration: none;
  color: inherit;
}
.clickable {
  cursor: pointer;
}
.clickable:hover {
  background-color: #f0f0f0;
}
</style>