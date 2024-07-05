<!-- 日時選択画面　フォームを送信 -->
<template>
  <div>
    <div class="title">
      <h1>Contact</h1>
      <h3>予約フォーム</h3>
    </div>
    <div class="message-under-title">
      <p>
        指定の日時を選択してください<br />
        ◎：予約可能　✖：予約不可<br />
        ※送信時にサービス規約に同意したものとみなします
      </p>
    </div>
    <div class="contactForm">
      <div class="form-group">
        <label for="datetime">■施術開始時刻</label><br />
        <div class="content">
          <div class="week-move">
            <div class="prev" @click="getPrevWeek">＜前週</div>
            <div class="next" @click="getNextWeek">翌週＞</div>
          </div>
          <table class="customer-rsv">
            <tr>
              <th>日付</th>
              <td class="head" v-for="day in display_days">
                <div class="date">{{ getDateMMDD(day) }}</div>
                <div class="dayofweek">{{ getDayofweek(day) }}</div>
              </td>
            </tr>
            <tr v-for="time in display_times">
              <th>{{ time }}</th>
              <td
                v-for="day in display_days"
                :style="{
                  cursor: reservable_dict[day]?.includes(time)
                    ? 'pointer'
                    : 'not-allowed',
                  background:
                    selected_datetime?.includes(day) &&
                    selected_datetime?.includes(time) &&
                    reservable_dict[day]?.includes(time)
                      ? '#fff3b8'
                      : reservable_dict[day]?.includes(time)
                      ? '#ffffff'
                      : '#d9d9d9',
                }"
                @click="
                  reservable_dict[day]?.includes(time)
                    ? setSelectedDatetime(day, time)
                    : null
                "
              >
                <p v-if="reservable_dict[day]?.includes(time)">◎</p>
                <p v-else>×</p>
              </td>
            </tr>
          </table>
        </div>
      </div>
      <button class="send" @click="postForm">送信</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import common from '@/plugins/common'

export default {
  data() {
    return {
      display_days: '',
      display_times: '',
      reservable_dict: '', // {20240214:[11:15,11:30,...], 20240215:[]}の形
      lineId: this.$route.query.lineid,
      fullname: this.$route.query.fullname,
      birthday: this.$route.query.birthday,
      gender: this.$route.query.gender,
      tel: this.$route.query.tel,
      serviceId: this.$route.query.service,
      selected_datetime: '', // 20240214 11:15の形
    }
  },
  mounted() {
    this.getDayList(new Date())
    this.getTimeList('11:00', '20:00', 15)
    //開発のためLIFFコメントアウト
    // this.$liffInit
    //   .then(() => {
    //     pass
    //   })
    //   .catch((error) => {
    //     this.liffError = error
    //   })
    this.getTimeList('11:00', '20:00', 15) // 営業時間、予約可能間隔の設定
    this.getReservableDict()
  },

  methods: {
    async getDayList(date) {
      const dayOfWeek = date.getDay()
      const difference = dayOfWeek === 0 ? -6 : 1 - dayOfWeek // 日曜日0~土曜6
      const firstDayOfWeek = new Date(date.setDate(date.getDate() + difference)) // 週の最初の日（月曜日）を設定

      const dayList = [] // 週の日付を格納する配列 YYYYMDD形式
      var focus_day = firstDayOfWeek
      for (let i = 0; i < 7; i++) {
        var focus_day = new Date(firstDayOfWeek.getTime())
        focus_day.setDate(focus_day.getDate() + i) // i日加算
        const formattedDate = `${focus_day.getFullYear()}${(
          focus_day.getMonth() + 1
        )
          .toString()
          .padStart(2, '0')}${focus_day.getDate().toString().padStart(2, '0')}`
        dayList.push(formattedDate)
      }
      this.display_days = dayList
    },

    async getTimeList(startTime, endTime, interval) {
      // NEXT:date型必要ない, 開始終了時間はDBから取得
      let result = []
      let current = new Date(`2024-01-01 ${startTime}`)
      const end = new Date(`2024-01-01 ${endTime}`)
      while (current < end) {
        result.push(this.formatTime(current))
        current = new Date(current.getTime() + interval * 60000) // 分をミリ秒に変換
      }
      this.display_times = result
    },

    setSelectedDatetime(day, time) {
      this.selected_datetime = `${day} ${time}`
    },

    formatTime(date) {
      let hours = date.getHours()
      let minutes = date.getMinutes()
      hours = hours < 10 ? '0' + hours : hours
      minutes = minutes < 10 ? '0' + minutes : minutes
      return `${hours}:${minutes}`
    },

    getDayofweek(yyyyMMdd) {
      const dateObj = this.parseYYYYMMDDToDate(yyyyMMdd)
      var date = new Date(dateObj)
      const dayOfWeek = date.getDay()
      const dayOfWeekStr = ['日', '月', '火', '水', '木', '金', '土'][dayOfWeek] // dateobjの番号順
      return dayOfWeekStr
    },

    getDateMMDD(yyyyMMdd) {
      const dateObj = this.parseYYYYMMDDToDate(yyyyMMdd)
      var date = new Date(dateObj)
      const month = date.getMonth() + 1
      const day = date.getDate()
      return `${month}/${day}`
    },

    parseYYYYMMDDToDate(yyyyMMdd) {
      const year = parseInt(yyyyMMdd.substring(0, 4), 10)
      const month = parseInt(yyyyMMdd.substring(4, 6), 10) - 1 // JSの月は0から始まるため1を引く
      const day = parseInt(yyyyMMdd.substring(6, 8), 10)
      return new Date(year, month, day)
    },

    async getPrevWeek() {
      const dateObj = this.parseYYYYMMDDToDate(this.display_days[0])
      var date = new Date(dateObj)
      date.setDate(date.getDate() - 7)
      this.getDayList(date)
      this.getReservableDict()
    },

    async getNextWeek() {
      const dateObj = this.parseYYYYMMDDToDate(this.display_days[6])
      var date = new Date(dateObj)
      date.setDate(date.getDate() + 1)
      this.getDayList(date)
      this.getReservableDict()
    },

    async getReservableDict() {
      // 初日のみを投げる
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservableList'
      const data = {
        display_first_day: this.display_days[0],
      }
      const response = await common.gateway_get(apiurl, data) // {20240214:[11:15,11:30,...], 20240215:[]}の形
      this.reservable_dict = response.reservable_dict
    },
    async postForm() {
      // ReservationListに送信
      var apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistReservationList'
      var data = {
        lineId: this.lineId,
        fullname: this.fullname,
        birthday: this.birthday,
        gender: this.gender,
        tel: this.tel,
        serviceId: this.service,
        supply_datetime: this.selected_datetime, //"20240214 11:15"の形
      }
      console.log('data completed')
      common.gateway_post(apiurl, data)
    },
  },
  // templateの選択
  layout: 'customer',
}
</script>

<style>
.week-move {
  display: flex;
  width: 100%;
  justify-content: space-between;
}
.prev　.next {
  color: #a19e9e;
  margin: 5px 0;
  border: none;
  cursor: pointer;
  width: 15%;
}
table.customer-rsv {
  border-collapse: separate;
  border-spacing: 3px;
  width: 100%;
}

.customer-rsv th,
.customer-rsv td {
  border-radius: 5px;
  text-align: center;
  padding: 3px 0;
}

.customer-rsv td.head {
  background-color: #ffffff;
  color: rgb(0, 0, 0);
}

.customer-rsv th {
  background-color: #ffffff;
  color: rgb(0, 0, 0);
  border: solid 1px #000000;
  width: 14%;
}

.customer-rsv td {
  background-color: #d9d9d9;
  border: solid 1px #636363;
  width: 10%;
}
table.supplier-rsv {
  font-size: 13px;
  border-collapse: separate;
  margin: 5px auto;
  text-align: center;
  border-spacing: 0px 8px;
  width: 100%;
}
.supplier-rsv td {
  background-color: #ffffff;
  border-top: solid 2px #ffffff;
  border-bottom: solid 2px #ffffff;
}
.supplier-rsv th,
.supplier-rsv td {
  padding: 2%;
  width: 10%;
}
</style>