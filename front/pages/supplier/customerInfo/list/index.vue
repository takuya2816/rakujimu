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
      <div class="list-header-item">来店の予定</div>
    </div>
    <div class="list-body">
      <div class="list-content">
        <div v-for="customer in customerList" :key="customer.id" class="list-record">
          <a :href="`/customer/${customer.id}`" class="customer-link">
            <div class="list-info">
              <div class="list-item">{{ customer.name }}</div>
              <div class="list-item">{{ customer.gender }}</div>
              <div class="list-item">{{ customer.lastReservedDate }}<br>{{ customer.lastReservedTime }}</div>
              <div class="list-item">{{ customer.nextReservedDate }}<br>{{ customer.nextReservedTime }}</div>
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
      reservationList: []
    }
  },
  mounted() {
    this.getCustomerMst()
  },
  methods:{
    async getCustomerMst(){
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetCustomerMst'
      const res = await common.gateway_get(apiurl)
      this.reservationList = res.Items  // TODO:変数の中身を確認して、for文を修正する
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