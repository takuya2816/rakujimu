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
                <label for="datetime">■施術開始時間</label>
                <div class="week-move">
                    <button class="prev" >前に</button>
                    <button class="next" >後に</button>
                </div>
                <table>
                    <tr>
                        <th>日付</th>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                    </tr>
                    <tr>
                        <th>11:00</th>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                    </tr>
                    <tr>
                        <th>11:15</th>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                    </tr>
                    <tr>
                    <th>11:30</th>
                    <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                    </tr>
                    <tr>
                    <th>見出し</th>
                    <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                        <td>〇</td>
                    </tr>
                </table>
            </div>
            <button class="send" @click="sendData">送信</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    // css: [
    //     '~/styles/reserve.css',
    // ],
    data() {
        return {
            accessToken: "",
        }
    },
    mounted() {
        this.$liffInit
        .then(() => {
            pass
        })
        .catch((error) => {
            this.liffError = error;
        });
    },

    methods: {
        async getAccessToken(){  // ユーザのaccesstokenを取得
            try {
                const accessToken = liff.getAccessToken();
                return accessToken
            } catch (error) {
                console.error(error);
                return null
            }
        },

        async getUserProfile(accessToken) {  // ユーザ情報を取得
            try {
                const response = await axios.get(`https://api.line.me/v2/profile`, {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`
                    }
                });
                this.lineId = response.data.userId;  // 各種を更新
                this.displayName = response.data.displayName;
                this.pictureUrl = response.data.pictureUrl;
            } catch (error) {
                console.error(error);
            }
        },
        async getUserInfo() {
            const accessToken = await this.getAccessToken();
            if (accessToken) {
                await this.getUserProfile(accessToken);
            }
        },

        async sendData() { // sendDataメソッドを非同期関数に変更
            console.log("sendData started");
            await this.getUserInfo();
            console.log("getUserInfo completed");
            var apiurl = "https://4om5vxifil.execute-api.ap-northeast-1.amazonaws.com/rakujimu-1/RegistCustomerMst";
            var data = {
                'id': 'test',  // ask:自動採番だからいらない
                'lineid': this.lineId,
                'name': document.getElementById('name').value,
                'date': document.getElementById('birthday').value,  // ask:dynamo dateになっている
                'address': document.getElementById('tel').value,  // ask:telへ変更
                'gender': document.getElementById('gender').value,
                'mailaddress': document.getElementById('email').value,
            };
            console.log("data completed");
            var jsonData = JSON.stringify(data);
            try {
                const response = await axios.post(apiurl, jsonData, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                alert(response.data);
            } catch (error) {
                alert(error);
            }
        },
    },
};
</script>