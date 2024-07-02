<!-- 予約詳細画面 -->

<template>
  <div>
    <div class="title">
      <h1>予約詳細</h1>
    </div>
    <div>
      <div class="detail-item">
        <span class="label">申込日時</span>
        <!-- <span class="value">{{ reservation_info.applicationDate }}</span> -->
      </div>
      <div class="detail-item">
        <span class="label">氏名</span>
        <!-- <span class="value">{{ reservation_info.name }}</span> -->
      </div>
      <div class="detail-item">
        <span class="label">メニュー</span>
        <!-- <span class="value">{{ reservation_info.menu }}</span> -->
      </div>
      <div class="detail-item">
        <span class="label">予約開始日時</span>
        <!-- <span class="value">{{ reservation_info.startDate }}</span> -->
      </div>
      <div class="detail-item">
        <span class="label">承認日時</span>
        <!-- <span class="value">{{ reservation_info.approvalDate || 'ー' }}</span> -->
      </div>
    </div>
    <div>
      <div class="buttons">
        <button @click="editReservation" class="edit-button">編集</button>
        <button @click="approveReservationInfo" class="post-button">承認</button>
      </div>
    </div>
  </div>
</template> 


<script>
export default {
  data() {
    return {
      reservation_info:{}
    }
  },
  mounted() {
    this.getCustomerInfo(this.$route.params.id)
  },
  methods: {
    async getCustomerInfo(reservation_id) {
      // 仮のAPIコールを実行し、予約情報を取得
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationInfo'
      const res = await Common.gateway_get(apiurl, reservation_id)
      this.customer_info = res.Items  // TODO:変数の中身を確認して、for文を修正する
    },

    async approveReservation(reservation_id) {
      // 承認ボタンが押されたときの処理
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistXXX'
      const res = await Common.gateway_post(apiurl, reservation_id)
    },

    editReservationInfo() {
      // 編集ボタンが押されたときの処理
      // TODO:予約IDを含めるcustomer_infoを次ページに渡す
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
