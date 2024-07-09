<template>
    <div>
        <div class="title">
            <h1>予約編集</h1>
        </div>
        <div class="reservation-edit">
            <div class="profile">
                <div class="profile-info">
                    <div class="detail-item">
                        <span class="label">申込日時</span>
                        <span class="value">{{ reservation.regist_datetime | datetime2date }} {{
                            reservation.regist_datetime |
                            datetime2hhmm }}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">氏名</span>
                        <span class="value">{{ reservation.customer_name }}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">メニュー</span>
                        <span class="value">
                            <select id="service_name" v-model="reservation.service_id" required>
                                <option v-for="item in servicelist" :key="item.id" :value="item.id">
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
                        <button class="cancel-button" @click="returnReservationDetail">キャンセル</button>
                        <button class="post-button" @click="removeReservation">削除</button>
                    </div>
                </div>
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
            reservation: {regist_datetime: '', customer_name: '', service_id: '', reserve_date: '', reserve_sttime: '', id: ''},
            servicelist: []
        }
    },
    async mounted() {
        // 開発のためliffコメントアウト
        this.$liffInit
          .then(() => {
            this.idToken = liff.getIDToken();
          })
          .catch((error) => {
            this.liffError = error
          });
        try {
            await this.getServiceList();
            await this.getReservationInfo(this.$route.params.id);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    },
    methods: {
        async getServiceList() {
            const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetServiceMst'
            const res = await common.gateway_get(apiurl)
            this.servicelist = res.Items
        },
        async getReservationInfo(reservationId) {
            try {
                const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
                const data = { reservation_id: [reservationId] }
                const res = await common.gateway_get(apiurl, data)
                this.reservation = res.Items[0]
            } catch (error) {
                console.error('Error fetching reservation info:', error);
            }
        },
        async updateReservation() {
            try {
                const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistReservationList'
                const res = await common.gateway_post(apiurl, this.reservation)
                if (res && res.result === "ok") {
                    // 保存成功時の処理
                    this.$router.push(`/reservedInfo/detail/${this.$route.params.id}`)
                } else {
                    // レスポンスが期待通りでない場合の処理
                    console.error('Unexpected response:', res)
                    alert('保存に失敗しました。予期せぬレスポンスを受け取りました。')
                }
            } catch (error) {
                // エラーハンドリング
                console.error('Error updating reservation:', error)
                alert('保存中にエラーが発生しました: ' + error.message)
            }
        },
        async removeReservation(reservation) {
            this.reservation.delete_flag = "true"
            try {
                const apiurl =
                'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistReservationList'
                const res = await common.gateway_post(apiurl, this.reservation)
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
        returnReservationDetail() {
            this.$router.push(`/reservedInfo/detail/${this.$route.params.id}`)
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
    }
}
</script>

<style scoped>
.reservation-edit {
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 8px;
}

.profile-info {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
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