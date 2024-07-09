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
      <div class="list-header-item">     </div>
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
          <a :href="`/approve/${reservation.id}`" class="reservation-approve">承認</a>
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
      reservationList: [],
      customerMst:{},
      serviceMst:{},
    }
  },
  mounted() {
    this.$liffInit
      .then(() => {
        this.idToken = liff.getIDToken();
      })
      .catch((error) => {
        this.liffError = error
      })
    this.getReservationList();
  },
  methods:{
    async getReservationList(){  // getCustomerMst, serviceMstから名前を引用したリストを取得
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
      const res = await common.gateway_get(apiurl)
      this.reservationList = res.Items
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