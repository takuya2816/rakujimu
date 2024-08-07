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
      <div class="list-header-item">操作</div>
    </div>
    <div class="list-body">
      <div v-for="reservation in sortedReservations" :key="reservation.id" class="list-record">
        <div class="reservation-link" @click="displayReserveDetail(reservation.id)">
          <div class="list-item">{{ reservation.regist_datetime | datetime2date }}<br>{{ reservation.regist_datetime | datetime2hhmm }}</div>
          <div class="list-item">{{ reservation.reserve_date }}<br>{{ reservation.reserve_sttime | hhmmss2hhmm }}</div>
          <div class="list-item">{{ reservation.customer_name }}</div>
          <div class="list-item">{{ reservation.service_name }}</div>
          <div class="list-item">
            <button v-if="reservation.approval_flag === 'false'" @click.stop="approveReservation(reservation)" class="reservation-approve">承認</button>
          </div>
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
      reservationList: [],
      customerMst:{},
      serviceMst:{},
      sortKey: 'regist_datetime', // デフォルトのソートキー
      sortOrder: 'desc' // デフォルトのソート順序
    }
  },
  mounted() {
    // 開発のためliffコメントアウト
    // this.$liffInit
    // .then(() => {
    //   this.idToken = liff.getIDToken();
    // })
    // .catch((error) => {
    //   this.liffError = error
    // })
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
    },
    displayReserveDetail(reservation_id){
      // 予約詳細画面に遷移
      this.$router.push(`/reservedInfo/detail/${reservation_id}`)
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

.list-header-item, .list-item {
  text-align: center; /* 中央揃え */
}

.list-body {
  display: flex;
  flex-direction: column;
  max-height: 400px; /* 高さを固定 */
  overflow-y: auto; /* 縦スクロールを有効にする */
}

.list-header, .list-record {
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 各カラムを均等に分割 */
  align-items: center; /* 垂直方向の中央揃え */
  padding: 10px 0;
  text-align: center; /* 中央揃え */
}

.reservation-link {
  display: contents; /* 親要素としてのレイアウト影響を排除 */
  cursor: pointer; /* クリック可能なカーソル */
}

.reservation-approve {
  padding: 5px 10px;
  background-color: #ccc;
  border-radius: 5px;
  text-decoration: none;
  color: #333;
  font-size: 14px;
  cursor: pointer;
}

.reservation-approve:hover {
  background-color: #aaa;
}

.list-record:hover {
  background-color: #f0f0f0;
}

.list-item {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
}

</style>