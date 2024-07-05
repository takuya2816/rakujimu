<template>
    <div>
        <div class="title">
            <h1>予約編集</h1>
        </div>
        <div class="details">
            <div class="detail-item">
                <span class="label">申込日時</span>
                <span class="value">{{ reservation.regist_datetime }}</span>
            </div>
            <div class="detail-item">
                <span class="label">氏名</span>
                <span class="value"><input id="customer_name" v-model="reservation.customer_name" required></span>
            </div>
            <div class="detail-item">
                <span class="label">メニュー</span>
                <span class="value">
                    <select id="service_name" v-model="reservation.service_name" required>
                        <option v-for="item in servicelist" :key="item.id" :value="item.name">
                            {{ item.name }}
                        </option>
                    </select>
                </span>
            </div>
            <div class="detail-item">
                <span class="label">予約日</span>
                <span class="value">
                    <input id="reserveDate" v-model="reservation.reserve_date" type="date" required>
                </span>
            </div>
            <div class="detail-item">
                <span class="label">予約時間</span>
                <span class="value">
                    <input id="reserveTime" v-model="reservation.reserve_sttime" type="time" required>
                </span>
            </div>
            <div class="buttons">
                <button class="post-button" @click="updateReservation">更新</button>
                <!-- <button @click="return" class="back-button">戻る</button> -->
                <button class="cancel-button" @click="cancelReservation">キャンセル</button>
            </div>
        </div>
    </div>
</template>

<script>
import common from '@/plugins/common'

export default {
    layout: 'supplier',
    data() {
        return {
            reservation: {
                customer_name: '',
                service_name: '',
                reserve_date: '',
                reserve_sttime: '',
                regist_datetime: ''
            },
            servicelist: []
        }
    },
    async mounted() {
        // 開発のためliffコメントアウト
        // this.$liffInit
        //   .then(() => {
        //     this.idToken = liff.getIDToken();
        //     // this.accessToken = liff.getAccessToken();
        //   })
        //   .catch((error) => {
        //     this.liffError = error
        //   })
        await this.getServiceList()
        await this.getReservationInfo(this.$route.params.id)
    },
    methods: {
        async getServiceList() {
            const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetServiceMst'
            const res = await common.gateway_get(apiurl)
            this.servicelist = res.Items
        },
        async getReservationInfo(reservationId) {
            const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
            const data = { reservationId: [reservationId] }
            const res = await common.gateway_get(apiurl, data)
            this.reservation = res.Items[0]  // リスト要素の1つ目を抽出
        },
        async updateReservation() {
            const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistReservationList'
            const res = await common.gateway_post(apiurl, this.reservation)
            if (res && res.result === "ok") {
                // 保存成功時の処理
                this.$router.push(`/reservedInfo/detail/${this.$route.params.id}`)
            } else {
                // エラー処理
                alert('保存に失敗しました。')
            }
        },
        cancelReservation() {
            this.$router.push(`/reservedInfo/detail/${this.$route.params.id}`)
        },
    },
}
</script>

<style scoped>
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

.detail-item input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.edit-form {
    max-width: 500px;
    margin: 0 auto;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
    color: #999;
}

input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}
</style>