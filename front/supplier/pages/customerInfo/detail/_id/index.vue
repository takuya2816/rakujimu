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
            <span class="value">{{ customer.name }}</span>
          </div>
          <div class="detail-item">
            <span class="label">性別</span>
            <span class="value">{{ customer.gender }}</span>
          </div>
          <div class="detail-item">
            <span class="label">生年月日</span>
            <span class="value">{{ customer.birthday }}</span>
          </div>
          <div class="detail-item">
            <span class="label">電話</span>
            <span class="value">{{ customer.tel }}</span>
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
            <a :href="`/reservedInfo/detail/${reservation.id}`" class="reservation-link">
              <div class="list-info">
                <div class="list-item">{{ reservation.regist_datetime | datetime2date }}<br>{{ reservation.regist_datetime | datetime2hhmm }}</div>
                <div class="list-item">{{ reservation.reserve_date }}<br>{{ reservation.reserve_sttime | hhmmss2hhmm }}</div>
                <div class="list-item">{{ reservation.customer_name }}</div>
                <div class="list-item">{{ reservation.service_name }}</div>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
    <div class="buttons">
      <button class="edit-button" @click="editCustomerInfo">編集</button>
      <button class="return-button" @click="returnCustomerList">一覧へ戻る</button>
    </div>
  </div>
</template> 


<script>
import common from '@/plugins/common'
export default {
  layout: 'supplier',
  data() {
    return {
      customer:{},
      reservationList:[]
    }
  },
  mounted() {
    this.getCustomerMst(this.$route.params.id)
    this.getReservationList(this.$route.params.id)
  },
  methods: {
    async getCustomerMst(customerId) {
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetCustomerMst'
      const data = {customerId: [customerId]}
      const res = await common.gateway_get(apiurl, data)
      this.customer = res[0]
    },

    async getReservationList(customerId) {
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
      const data = {customerId: [customerId]}
      const res = await common.gateway_get(apiurl, data)
      this.reservationList = res.Items
    },

    editCustomerInfo(customerId) {
      // 編集ボタンが押されたときの処理
      this.$router.push(`/customerInfo/detail/${this.$route.params.id}/edit`)
    },
    returnCustomerList(){
      // 一覧へ戻るボタンが押されたときの処理
      this.$router.push(`/customerInfo/list`)
    }
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
      const date = new Date(value);
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${hours}:${minutes}`;
    },
    hhmmss2hhmm(value) {
      if (!value) return '';
      const [hours, minutes] = value.split(':');
      return `${hours}:${minutes}`;
    }
  },
}
</script>

<style>
.details {
  margin-bottom: 20px;
}
.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px; /* 項目ごとの間隔を広げる */
}
.detail-item .label {
  color: #999;
  flex-basis: 40%;
  text-align: right; /* 右揃えにする */
  margin-right: 20px;
}
.detail-item .value {
  color: #333;
  flex-basis: 60%;
  text-align: left;
}
</style>
