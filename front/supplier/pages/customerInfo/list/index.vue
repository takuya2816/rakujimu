<!-- 顧客一覧画面 -->
<template>
  <div>
    <div class="title">
      <h1>顧客一覧</h1>
    </div>
    <div class="list-header">
      <div class="list-header-item">氏名</div>
      <div class="list-header-item">性別</div>
      <div class="list-header-item">最終来店日</div>
      <div class="list-header-item">次の予約</div>
    </div>
    <div class="list-body">
      <div class="list-content">
        <div v-for="customer in customerMst" :key="customer.id" class="list-record">
          <a :href="`/customerInfo/detail/${customer.id}`" class="customer-link">
            <div class="list-info">
              <div class="list-item">{{ customer.name }}</div>
              <div class="list-item">{{ customer.gender }}</div>
              <div class="list-item">{{ customer.lastReservedDate | datetime2date }}<br>{{ customer.lastReservedSttime}}</div>
              <div class="list-item">{{ customer.nextReservedDate | datetime2date }}<br>{{ customer.nextReservedSttime}}</div>
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import common from '@/plugins/common'
export default {
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
      customerMst: []
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
  },
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
}
</script>

<style>
  .customer-link {
    display: flex;
    flex-grow: 1;
    text-decoration: none;
    color: inherit;
  }
</style>