<template>
    <div>   
        <div class="title">
            <h1>Contact</h1>
            <h3>予約フォーム</h3>
        </div>
        <div class="message">
            <p>
                XXXXXXの予約申込を行います<br>
                予約確定後に、店舗からご連絡申し上げます<br>
                ※送信時にサービス規約に同意したものとみなします
            </p>
        </div>
        <div class="contactForm">
            <div class="form-group">
                <label for="name">■お名前</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="birthday">■生年月日</label>
                <input type="text" id="birthday" name="birthday" required>
            </div>
            <div class="form-group">
                <label for="gender">■性別</label>
                <input type="text" id="gender" name="gender" required>
            </div>
            <div class="form-group">
                <label for="tel">■電話</label>
                <input type="text" id="tel" name="tel">
            </div>
            <div class="form-group">
                <label for="menu">■メニュー</label>
                <select id="menu" name="menu" required>
                    <option value="1">カット</option>
                    <option value="2">カラー</option>
                    <option value="3">パーマ</option>
                </select>
            </div>
            <button class="send" @click="reserve">日時選択へ</button>
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
        reserve() {
            this.$router.push("/reserving");
        },
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