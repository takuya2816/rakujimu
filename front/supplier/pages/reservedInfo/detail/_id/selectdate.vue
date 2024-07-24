<!-- 日時変更時 ポップアップ表示 -->
<template>
    <div class="popup-overlay">
      <div class="popup-content">
        <button class="close-button" @click="closePopup">×</button>
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
                      cursor: reservable_dict[day]?.includes(time) ? 'pointer' : 'not-allowed',
                      background:
                        reserveStDatetime?.includes(day) &&
                        reserveStDatetime?.includes(time) &&
                        reservable_dict[day]?.includes(time)
                          ? '#fff3b8'
                          : reservable_dict[day]?.includes(time)
                          ? '#ffffff'
                          : '#d9d9d9',
                    }"
                    @click="reservable_dict[day]?.includes(time) ? setSelectedDatetime(day, time) : null"
                  >
                    <p v-if="reservable_dict[day]?.includes(time)">◎</p>
                    <p v-else>×</p>
                  </td>
                </tr>
              </table>
            </div>
          </div>
          <button class="send" @click="postForm">決定</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import common from '@/plugins/common'
  
  export default {
    props: {
      service_id: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        display_days: [],
        display_times: [],
        reservable_dict: {}, // {20240214:[11:15,11:30,...], 20240215:[]}の形
        reserveStDatetime: '', // 20240214 11:15の形
      }
    },
    mounted() {
      this.getTimeList('11:00', '20:00', 15); // 営業時間、予約可能間隔の設定
      this.getDayList(new Date());
      this.getReservableDict();
    },
    methods: {
      closePopup() {
        this.$emit('close');
      },
      async getDayList(date) {
        const dayOfWeek = date.getDay();
        const difference = dayOfWeek === 0 ? -6 : 1 - dayOfWeek; // 日曜日0~土曜6
        const firstDayOfWeek = new Date(date.setDate(date.getDate() + difference)); // 週の最初の日（月曜日）を設定
  
        const dayList = []; // 週の日付を格納する配列 YYYYMMDD形式
        for (let i = 0; i < 7; i++) {
          const focus_day = new Date(firstDayOfWeek.getTime());
          focus_day.setDate(focus_day.getDate() + i); // i日加算
          const formattedDate = `${focus_day.getFullYear()}${(focus_day.getMonth() + 1).toString().padStart(2, '0')}${focus_day.getDate().toString().padStart(2, '0')}`;
          dayList.push(formattedDate);
        }
        this.display_days = dayList;
      },
      async getTimeList(startTime, endTime, interval) {
        let result = [];
        let current = new Date(`2024-01-01 ${startTime}`);
        const end = new Date(`2024-01-01 ${endTime}`);
        while (current < end) {
          result.push(this.formatTime(current));
          current = new Date(current.getTime() + interval * 60000); // 分をミリ秒に変換
        }
        this.display_times = result;
      },
      setSelectedDatetime(day, time) {
        this.reserveStDatetime = `${day} ${time}`;
      },
      formatTime(date) {
        let hours = date.getHours();
        let minutes = date.getMinutes();
        hours = hours < 10 ? '0' + hours : hours;
        minutes = minutes < 10 ? '0' + minutes : minutes;
        return `${hours}:${minutes}`;
      },
      getDayofweek(yyyyMMdd) {
        const dateObj = this.parseYYYYMMDDToDate(yyyyMMdd);
        const dayOfWeek = dateObj.getDay();
        const dayOfWeekStr = ['日', '月', '火', '水', '木', '金', '土'][dayOfWeek]; // dateObjの番号順
        return dayOfWeekStr;
      },
      getDateMMDD(yyyyMMdd) {
        const dateObj = this.parseYYYYMMDDToDate(yyyyMMdd);
        const month = dateObj.getMonth() + 1;
        const day = dateObj.getDate();
        return `${month}/${day}`;
      },
      parseYYYYMMDDToDate(yyyyMMdd) {
        const year = parseInt(yyyyMMdd.substring(0, 4), 10);
        const month = parseInt(yyyyMMdd.substring(4, 6), 10) - 1; // JSの月は0から始まるため1を引く
        const day = parseInt(yyyyMMdd.substring(6, 8), 10);
        return new Date(year, month, day);
      },
      async getPrevWeek() {
        const dateObj = this.parseYYYYMMDDToDate(this.display_days[0]);
        var date = new Date(dateObj);
        date.setDate(date.getDate() - 7);
        this.getDayList(date);
        this.getReservableDict();
      },
      async getNextWeek() {
        const dateObj = this.parseYYYYMMDDToDate(this.display_days[6]);
        var date = new Date(dateObj);
        date.setDate(date.getDate() + 1);
        this.getDayList(date);
        this.getReservableDict();
      },
      async getReservableDict() {
        // 初日のみを投げる
        var apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservableList';
        var data = {
          first_day_of_week: this.display_days[0],
          service_id: this.service_id
        };
        var response = await common.gateway_get(apiurl, data);
        this.reservable_dict = response.reservable_dict;  // {20240214:[11:15,11:30,...], 20240215:[]}の形
      },
      async postForm() {
        // 予約データを親コンポーネントに送信
        this.$emit('update-date', this.reserveStDatetime);
        this.closePopup();
      },
    },
  }
  </script>
  
  <style scoped>
  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .popup-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 90%;
    max-width: 600px; /* サイズを小さくする */
    max-height: 90vh; /* 高さの制限を追加 */
    overflow-y: auto; /* 縦スクロールを有効にする */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    position: relative;
  }
  
  .close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    border: none;
    background: none;
    font-size: 20px;
    cursor: pointer;
  }
  
  .contactForm {
    width: 100%;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .week-move {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  
  .customer-rsv {
    width: 100%;
    border-collapse: collapse;
  }
  
  .customer-rsv th,
  .customer-rsv td {
    border: 1px solid #ddd;
    text-align: center;
    padding: 8px;
  }
  
  .customer-rsv th {
    background-color: #f2f2f2;
  }
  
  .send {
    margin-top: 15px;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>