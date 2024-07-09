<!-- 予約一覧画面 -->
<template>
  <div>
    <div class="title">
      <h1>予約一覧</h1>
    </div>
    <div class="list-header">
      <div class="list-header-item clickable" @click="sortBy('regist_datetime')">
        申込日時 <span v-if="sortKey === 'regist_datetime'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
      </div>
      <div class="list-header-item clickable" @click="sortBy('reserve_date')">
        予約日時 <span v-if="sortKey === 'reserve_date'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
      </div>
      <div class="list-header-item clickable" @click="sortBy('customer_name')">
        氏名 <span v-if="sortKey === 'customer_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
      </div>
      <div class="list-header-item clickable" @click="sortBy('service_name')">
        メニュー <span v-if="sortKey === 'service_name'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
      </div>
      <div class="list-header-item">     </div>
    </div>
    <div class="list-body">
      <div class="list-content">
        <div v-for="reservation in sortedReservations" :key="reservation.id" class="list-record">
          <a :href="`/reservedInfo/detail/${reservation.id}`" class="reservation-link">
            <div class="list-info">
              <div class="list-item">{{ reservation.regist_datetime | datetime2date }}<br>{{ reservation.regist_datetime | datetime2hhmm }}</div>
              <div class="list-item">{{ reservation.reserve_date }}<br>{{ reservation.reserve_sttime | hhmmss2hhmm }}</div>
              <div class="list-item">{{ reservation.customer_name }}</div>
              <div class="list-item">{{ reservation.service_name }}</div>
            </div>
          </a>
          <button v-if="reservation.approval_flag === 'false'" @click="approveReservation(reservation)" class="reservation-approve">承認</button>
        </div>
      </div>
    </div>
    <div class="buttons">
      <button class="edit-button" @click="returnIndex">戻る</button>
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
      sortKey: 'regist_datetime', // デフォルトのソートキー
      sortOrder: 'desc' // デフォルトのソート順序
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
  computed: {
    sortedReservations() {
      return [...this.reservationList].sort((a, b) => {
        let aValue = a[this.sortKey];
        let bValue = b[this.sortKey];
        
        // 日付型の場合、比較前に Date オブジェクトに変換
        if (this.sortKey === 'regist_datetime' || this.sortKey === 'reserve_date') {
          aValue = new Date(aValue);
          bValue = new Date(bValue);
        }
        
        if (aValue < bValue) return this.sortOrder === 'asc' ? -1 : 1;
        if (aValue > bValue) return this.sortOrder === 'asc' ? 1 : -1;
        return 0;
      });
    }
  },
  methods:{
    async getReservationList(){  // getCustomerMst, serviceMstから名前を引用したリストを取得
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
      const res = await common.gateway_get(apiurl)
      this.reservationList = res.Items
    },
    async approveReservation(reservation) {
      // 承認ボタンが押されたときの処理
      try {
        reservation.approval_flag = "true"
        var apiurl =
          'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistReservationList'
        var data = {
          id: reservation.id,
          customer_name: reservation.customer_name, 
          service_id: reservation.service_id, 
          reserve_date: reservation.reserve_date,
          reserve_sttime: reservation.reserve_sttime, 
          approval_flag: reservation.approval_flag,
          delete_flag: "false",
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
    returnIndex(){
      this.$router.push(`/`)
    },
    sortBy(key) {
      if (this.sortKey === key) {
        // 同じキーでソートする場合は順序を反転
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        // 新しいキーでソートする場合は昇順から開始
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
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
.clickable {
  cursor: pointer;
}
.clickable:hover{
  background-color: #f0f0f0;
}
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