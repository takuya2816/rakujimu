<!-- 日時選択画面　フォームを送信 -->
<template>
    <div>   
        <div class="title">
            <h1>Contact</h1>
            <h3>予約フォーム</h3>
        </div>
        <div class="message">
            <p>
                指定の日時を選択してください<br>
                ◎：予約可能　✖：予約不可<br>
                ※送信時にサービス規約に同意したものとみなします
            </p>
        </div>
        <div class="contactForm">
            <div class="form-group">
                <label for="datetime">■施術開始時刻</label><br>
                <div class="content">
                    <div class="week-move">
                        <div class="prev" @click="getPrevWeek" >＜前週</div>
                        <div class="next" @click="getNextWeek">翌週＞</div>
                    </div>
                    <table>
                        <tr>
                            <th>日付</th>
                            <td class="head" v-for="day in display_days">
                                <div class="date">{{ getDateStr(day) }}</div>
                                <div class="dayofweek">{{ getDayofweek(day) }}</div>
                            </td>
                        </tr>
                        <tr v-for="times in display_times">
                            <th>{{ times }}</th>
                            <tr v-for="day in display_days">
                                <td v-if="reservable_dict[day].includes(times)">◎</td>
                                <td v-else>×</td>
                            </tr>
                        </tr>
                    </table>
                </div>
            </div>
            <button class="send" @click="postForm">送信</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Common from '@/plugins/common'

export default {
    data() {
        return {
            display_days: "",
            display_times: "",
            reservable_dict: "",  // {2024-02-14:[11:15,11:30,...], 2024-02-15:[]}の形
            fullname: "",
            birthday: "",
            gender: "",
            tel: "",
            menu: "",
        }
    },
    mounted() {
        this.getDayList(new Date());
        this.getTimeList('11:00', '20:00', 15);

        this.$liffInit
        .then(() => {
            pass
        })
        .catch((error) => {
            this.liffError = error;
        });
    },

    methods: {
        async getDayList(date) {
            const dayOfWeek = date.getDay();
            const difference = dayOfWeek === 0 ? -6 : 1 - dayOfWeek; // 日曜日0~土曜6
            const firstDayOfWeek = new Date(date.setDate(date.getDate() + difference));  // 週の最初の日（月曜日）を設定
            
            const dayList = [];  // 週の日付を格納する配列
            var focus_day = firstDayOfWeek
            for (let i = 0; i < 7; i++) {
                var focus_day = new Date(firstDayOfWeek.getTime());
                focus_day.setDate(focus_day.getDate() + i); // i日加算
                dayList.push(focus_day);
            }
            this.display_days = dayList;
        },

        async getTimeList(startTime, endTime, interval) {  // NEXT:date型の必要ない
            let result = [];
            let current = new Date(`2024-01-01 ${startTime}`);
            const end = new Date(`2024-01-01 ${endTime}`);
            while (current <= end) {
                result.push(this.formatTime(current));
                current = new Date(current.getTime() + interval * 60000); // 分をミリ秒に変換
            }
            this.display_times = result;
        },

        formatTime(date) {
            let hours = date.getHours();
            let minutes = date.getMinutes();
            hours = hours < 10 ? '0' + hours : hours;
            minutes = minutes < 10 ? '0' + minutes : minutes;
            return `${hours}:${minutes}`;
        },

        getDayofweek(date) {
            const dayOfWeek = date.getDay();
            const dayOfWeekStr = [ "日", "月", "火", "水", "木", "金", "土"][dayOfWeek];
            return dayOfWeekStr;
        },

        getDateStr(date) {
            const month = date.getMonth() + 1;
            const day = date.getDate();
            return `${month}/${day}`;
        },

        async getPrevWeek() {
            var date = new Date(this.display_days[0]);
            date.setDate(date.getDate()-7);
            this.getDayList(date);
            this.getReservableList();
        },

        async getNextWeek() {
            var date = new Date(this.display_days[6]);
            date.setDate(date.getDate()+1);
            this.getDayList(date);
            this.getReservableList();
        },

        async getReservableList() {  // TODO
            const apiurl = "https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservableList";
            const data = {
                'display_days': this.display_days,
            };
            const response = await Common.gateway_get(apiurl, data);  // TODO:{2024-02-14:[11:15,11:30,...], 2024-02-15:[]}の形
            this.reservable_dict = response.data.reservable_dict;
        },
        async postForm() {
            await this.getUserInfo();
            console.log("getUserInfo completed");
            var apiurl = "https://4om5vxifil.execute-api.ap-northeast-1.amazonaws.com/rakujimu-1/RegistCustomerMst";
            var data = {
                'id': 'test',
                'lineid': this.lineId,
                'fullname': document.getElementById('fullname').value,
                'date': document.getElementById('birthday').value,  // ask:dynamo dateになっている
                'address': document.getElementById('tel').value,
                'gender': document.getElementById('gender').value,
                'mailaddress': document.getElementById('email').value,
            };
            console.log("data completed");
            Common.gateway_post(apiurl, data);
        },
    },
};
</script>