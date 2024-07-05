<!-- 予約詳細画面 -->

<template>
  <div>
    <div class="title">
      <h1>予約詳細</h1>
    </div>
    <div class="details">
      <div class="detail-item">
        <span class="label">申込日時</span>
        <span class="value">{{ reservation.regist_datetime | datetime2date }} {{ reservation.regist_datetime | datetime2hhmm }}</span>
      </div>
      <div class="detail-item">
        <span class="label">氏名</span>
        <span class="value">{{ reservation.customer_name }}</span>
      </div>
      <div class="detail-item">
        <span class="label">メニュー</span>
        <span class="value">{{ reservation.service_name }}</span>
      </div>
      <div class="detail-item">
        <span class="label">予約開始日時</span>
        <span class="value">{{ reservation.reserve_date }} {{ reservation.reserve_sttime | hhmmss2hhmm }}</span>
      </div>
      <div class="detail-item">
        <span class="label">承認日時</span>
        <span class="value">{{ reservation.approval_flag || 'ー' }}</span>
      </div>
    </div>
    <div>
      <div class="buttons">
        <button @click="editReservationInfo" class="edit-button">編集</button>
        <button @click="approveReservation" class="post-button">承認</button>
      </div>
    </div>
  </div>
</template> 


<script>
import common from '@/plugins/common'
export default {
  data() {
    return {
      reservation:{}
    }
  },
  mounted() {
    this.getReservationInfo(this.$route.params.id)
  },
  methods: {
    async getReservationInfo(reservationId) {
      // 仮のAPIコールを実行し、予約情報を取得
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
      const data = { reservationId: [reservationId] }
      const res = await common.gateway_get(apiurl, data)
      this.reservation = res.Items[0]  // リスト要素の1つ目を抽出
    },

    async approveReservation(reservationId) {
      // 承認ボタンが押されたときの処理
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistXXX'
      const data = { reservationId: reservationId }
      const res = await common.gateway_get(apiurl, data)
    },
    
    editReservationInfo() {
      // 編集ボタンが押されたときの処理
      this.$router.push(`/reservedInfo/detail/${this.$route.params.id}/edit`)
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
