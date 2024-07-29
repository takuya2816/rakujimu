<!-- 予約詳細画面 -->

<template>
  <div>
    <div class="title">
      <h1>予約詳細</h1>
    </div>
    <div class="details">
      <div class="detail-item">
        <span class="label">申込日時</span>
        <span class="value">{{ datetime2date(reservation.regist_datetime) }} {{ datetime2hhmm(reservation.regist_datetime) }}</span>
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
        <span class="value">{{ reservation.reserve_date }} {{ hhmmss2hhmm(reservation.reserve_sttime) }}</span>
      </div>
      <div class="detail-item">
        <span class="label">メモ</span>
        <span class="value">{{ reservation.memo }}</span>
      </div>
      <div class="detail-item">
        <span class="label">承認日時</span>
        <span class="value">{{ reservation.approval_flag == "true" ? datetime2date(reservation.approval_datetime)+" "+datetime2hhmm(reservation.approval_datetime) : '-' }}</span>
      </div>
    </div>
    <div>
      <div class="buttons">
        <button class="return-button" @click="returnReservationList">一覧へ戻る</button>
        <button class="edit-button" @click="editReservationInfo">編集</button>
        <button v-if="reservation.approval_flag === 'false'" @click="approveReservation" class="post-button">承認</button>
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
    // 開発のためliffコメントアウト
    // this.$liffInit
    //   .then(() => {
    //     this.idToken = liff.getIDToken();
    //   })
    //   .catch((error) => {
    //     this.liffError = error
    //   });
    this.getReservationInfo(this.$route.params.id)
  },
  methods: {
    async getReservationInfo(reservationId) {
      // 仮のAPIコールを実行し、予約情報を取得
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
      const data = { reservation_id: reservationId }
      console.log(data)
      const res = await common.gateway_get(apiurl, data)
      this.reservation = res.Items[0]  // リスト要素の1つ目を抽出
    },

    async approveReservation() {
      // 承認ボタンが押されたときの処理
      try {
        this.reservation.approval_change_flag = "true"
        this.reservation.approval_flag = "true"
        var apiurl =
          'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistReservationList'
        var data = {
          id: this.reservation.id,
          customer_name: this.reservation.customer_name, 
          service_id: this.reservation.service_id, 
          reserve_date: this.reservation.reserve_date,
          reserve_sttime: this.reservation.reserve_sttime, 
          approval_flag: this.reservation.approval_flag,
          memo: this.reservation.memo,
          delete_flag: "false",
          approval_change_flag: "true"
        };
        console.log(JSON.stringify(data))
        var res = await common.gateway_post(apiurl, data)  // TODO:リクエストクエリに含めたいがparamsでかえってきてしまう
        if (res && res.result === "ok") {
          // 承認成功時の処理
          this.$router.push(`/reservedInfo/list`)
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
    returnReservationList() {
      // 一覧へ戻るボタンが押されたときの処理
      this.$router.push(`/reservedInfo/list`)
    },
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
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: #ffffff;
  padding: 20px 5px;
  border-radius: 8px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  margin-bottom: 10px;
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
