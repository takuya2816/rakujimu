<!-- 予約詳細画面 -->

<template>
  <div>
    <div class="title">
      <h1>予約詳細</h1>
    </div>
    <div class="details">
      <div class="detail-item">
        <span class="label">申込日時</span>
        <span class="value">{{ reservation.regist_datetime | datetime2date }} {{ reservation.regist_datetime |
          datetime2hhmm }}</span>
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
        <button class="edit-button" @click="editReservationInfo">編集</button>
        <button class="post-button" @click="approveReservation">承認</button>
        <button class="post-button" @click="removeReservation">削除</button>
        <button class="post-button" @click="returnReservationList">一覧へ戻る</button>
      </div>
    </div>
  </div>
</template>


<script>
import common from '@/plugins/common'
export default {
  data() {
    return {
      reservation: {}
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

    async approveReservation(reservation) {
      // 承認ボタンが押されたときの処理
      reservation.approval_flag = "true"
      try {
        const apiurl =
          'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistReservationList'
        const data = { reservation }
        const res = await common.gateway_get(apiurl, data)
        if (res && res.result === "ok") {
          // 承認成功時の処理
          this.$router.push(`/reservedInfo/detail/${this.$route.params.id}`)
        } else {
          // レスポンスが期待通りでない場合の処理
          console.error('Unexpected response:', res)
          alert('承認に失敗しました。予期せぬレスポンスを受け取りました。')
        }
      } catch (error) {
        // エラーハンドリング
        console.error('Error saving customer info:', error)
        alert('保存中にエラーが発生しました。')
      }
    },

    editReservationInfo() {
      // 編集ボタンが押されたときの処理
      this.$router.push(`/reservedInfo/detail/${this.$route.params.id}/edit`)
    },

    async removeReservation(reservation) {
      reservation.delete_flag = "true"
      try {
        const apiurl =
          'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistReservationList'
        const data = { reservation }
        const res = await common.gateway_get(apiurl, data)
        if (res && res.result === "ok") {
          // 承認成功時の処理
          this.$router.push(`/reservedInfo/detail/${this.$route.params.id}`)
        } else {
          // レスポンスが期待通りでない場合の処理
          console.error('Unexpected response:', res)
          alert('承認に失敗しました。予期せぬレスポンスを受け取りました。')
        }
      } catch (error) {
        // エラーハンドリング
        console.error('Error saving customer info:', error)
        alert('保存中にエラーが発生しました。')
      }
    },

    returnReservationList() {
      // 一覧へ戻るボタンが押されたときの処理
      this.$router.push(`/reservedInfo/list`)
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
  margin-bottom: 20px;
  /* 項目ごとの間隔を広げる */
}

.detail-item .label {
  color: #999;
  flex-basis: 40%;
  text-align: right;
  /* 右揃えにする */
  margin-right: 20px;
}

.detail-item .value {
  color: #333;
  flex-basis: 60%;
  text-align: left;
}
</style>
