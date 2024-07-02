<!-- 予約一覧画面 -->
<template>
  <div>
    <div class="title">
      <h1>予約一覧</h1>
    </div>
    <div class="list-header">
      <div class="list-header-item">申込日時</div>
      <div class="list-header-item">予約日時</div>
      <div class="list-header-item">氏名</div>
      <div class="list-header-item">メニュー</div>
      <div class="list-header-item"></div>
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
          <a :href="`/approve/${reservation.id}`" class="reservation-approve">承認</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
    this.getReservationList()
  },
  methods:{
    async getReservationList(){
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
      const res = await Common.gateway_get(apiurl)
      this.reservationList = res.Items  // TODO:変数の中身を確認して、for文を修正する
    }
  },
  layout: 'supplier',
}
</script>

<style>
  .reservation-link {
    display: flex;
    flex-grow: 1;
    text-decoration: none;
    color: inherit;
  }
  .reservation-approve {
  padding: 5px 10px;
  background-color: #ccc;
  border-radius: 5px;
  text-decoration: none;
  color: #333;
  font-size: 14px;
  margin-left: 10px;
}

.reservation-approve:hover {
  background-color: #aaa;
}
</style>