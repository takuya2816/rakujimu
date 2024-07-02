<!-- 顧客詳細画面 -->

<template>
  <div>
    <div class="title">
      <h1>顧客詳細</h1>
    </div>
    <div class="customer-details">
      <div class="profile">
        <div class="profile-picture"></div>
        <div class="profile-info">
          <div class="detail-item">
            <span class="label">氏名</span>
            <span class="value">{{ customerInfo.name }}</span>
          </div>
          <div class="detail-item">
            <span class="label">性別</span>
            <span class="value">{{ customerInfo.gender }}</span>
          </div>
          <div class="detail-item">
            <span class="label">生年月日</span>
            <span class="value">{{ customerInfo.birthdate }}</span>
          </div>
          <div class="detail-item">
            <span class="label">住所</span>
            <span class="value">{{ customerInfo.address }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="reservation-history">
      <div class="list-header">
        <div class="list-header-item">申込日時</div>
        <div class="list-header-item">予約日時</div>
        <div class="list-header-item">氏名</div>
        <div class="list-header-item">メニュー</div>
      </div>
      <div class="list-body">
        <div class="list-content">
          <div v-for="reservation in reservationList" :key="reservation.id" class="list-record">
            <a :href="`/customer/${reservation.id}`" class="reservation-link">
              <div class="list-info">
                <div class="list-item">{{ reservation.applicationDate }}<br>{{ reservation.applicationTime }}</div>
                <div class="list-item">{{ reservation.startDate }}<br>{{ reservation.startTime }}</div>
                <div class="list-item">{{ reservation.name }}</div>
                <div class="list-item">{{ reservation.menu }}</div>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
    <div class="buttons">
      <button @click="editCustomerInfo" class="edit-button">編集</button>
    </div>
  </div>
</template> 


<script>
export default {
  data() {
    return {
      customerInfo:{},
      reservationList:[]
    }
  },
  mounted() {
    this.getCustomerInfo(this.$route.params.id)
  },
  methods: {
    async getCustomerInfo(customer_id) {
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationInfo'
      const res = await Common.gateway_get(apiurl, customer_id)
      this.customer_info = res.Items  // TODO:変数の中身を確認して、for文を修正する
    },

    async getCustomerReservationList(customer_id) {
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
      const res = await Common.gateway_get(apiurl, customer_id)
      this.reservationList = res.Items  // TODO:変数の中身を確認して、for文を修正する
    },

    async editCustomerInfo(customer_id) {
      // 承認ボタンが押されたときの処理
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistXXX'
      const res = await Common.gateway_post(apiurl, customer_id)
    },
  },
  layout: 'supplier',
}
</script>

<style>
.details {
  margin-bottom: 20px;
}
.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}
.detail-item .label {
  color: #999;
}
.detail-item .value {
  color: #333;
}
</style>
