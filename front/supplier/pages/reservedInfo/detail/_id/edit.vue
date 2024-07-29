<template>
    <div>
        <div class="title">
            <h1>予約編集</h1>
        </div>
        <div class="details">
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
                    <select id="service_name" v-model="temporaryServiceId" @change="handleServiceChange" required>
                        <option v-for="item in servicelist" :key="item.id" :value="item.id">
                            {{ item.name }}
                        </option>
                    </select>
                </span>
            </div>
            <div class="detail-item">
                <span class="label">予約開始日時</span>
                <span class="value clickable" @click="selectdatePop">{{ reservation.reserve_date }} {{ hhmmss2hhmm(reservation.reserve_sttime) }}</span>
                <!-- <i class="fas fa-pen"></i> -->
            </div>
        </div>
        <div class="buttons">
            <button class="cancel-button" @click="returnReservationDetail">キャンセル</button>
            <button class="post-button" @click="updateReservation">変更</button>
            <button class="post-button" @click="removeReservation">削除</button>
        </div>
        <!-- ポップアップ画面 -->
        <selectdate v-if="popupFlag" @close="closePopup" @update-date="updateDateTime" :service_id="temporaryServiceId" />
    </div>
</template>

<script>
import common from '@/plugins/common'
import selectdate from './selectdate.vue'

export default {
    layout: 'supplier',
    components: {
        selectdate
    },
    data() {
        return {
            reservation: {regist_datetime: '', customer_name: '', service_id: '', reserve_date: '', reserve_sttime: '', id: ''},
            servicelist: [],
            popupFlag: false,
            originalServiceId: '',
            originalReserveDate: '',
            originalReserveStTime: '',
            temporaryServiceId: ''  // メニュー変更用の一時的な変数
        }
    },
    async mounted() {
        // 開発のためliffコメントアウト
        // this.$liffInit
        //   .then(() => {
        //     this.idToken = liff.getIDToken();
        //   })
        //   .catch((error) => {
        //     this.liffError = error
        //   });
        await this.getServiceList();
        await this.getReservationInfo(this.$route.params.id);
    },
    methods: {
        async getServiceList() {
            const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetServiceMst'
            const res = await common.gateway_get(apiurl)
            this.servicelist = res.Items
        },
        async getReservationInfo(reservationId) {
            const apiurl =
                'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
            const data = { reservation_id: reservationId }
            console.log(data)
            const res = await common.gateway_get(apiurl, data)
            this.reservation = res.Items[0]  // リスト要素の1つ目を抽出
            // 元の値を保持
            this.originalServiceId = this.reservation.service_id;
            this.originalReserveDate = this.reservation.reserve_date;
            this.originalReserveStTime = this.reservation.reserve_sttime;
            this.temporaryServiceId = this.reservation.service_id;  // 一時的な変数に初期値を設定
        },
        selectdatePop() {
            this.popupFlag = true;
        },
        handleServiceChange() {
            // メニューが変更されたら、元の値を保持してポップアップを表示
            this.selectdatePop();
        },
        updateDateTime(newDateTime) {  // 子コンポーネントからのnewDateTimeの渡し方は正しいか
            console.log('newDateTime:', newDateTime);
            const [date, time] = newDateTime.split(' ');
            const year = date.substring(0, 4);
            const month = date.substring(4, 6);
            const day = date.substring(6, 8);
            const formattedDate = new Date(`${year}-${month}-${day}`).toISOString().split('T')[0];
            this.reservation.reserve_date = formattedDate;
            this.reservation.reserve_sttime = time;
            this.reservation.service_id = this.temporaryServiceId;  // 一時的なサービスIDを確定
            // ポップアップを閉じる
            this.popupFlag = false;
        },
        closePopup() {
            // ポップアップが閉じられたときに元の値に戻す
            this.temporaryServiceId = this.reservation.service_id;  // 一時的な変数に元の値を再設定
            this.popupFlag = false;
        },
        async updateReservation() {
            // メニュー・日時変更をしたい場合は画面遷移、それ以外の場合はpost
            try {
                const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistReservationList'
                console.log('reservation:', this.reservation)
                const res = await common.gateway_post(apiurl, this.reservation)
                if (res && res.result === "ok") {
                    this.$router.push(`/reservedInfo/detail/${this.$route.params.id}`)
                } else {
                    console.error('Unexpected response:', res)
                    alert('保存に失敗しました。予期せぬレスポンスを受け取りました。')
                }
            } catch (error) {
                console.error('Error updating reservation:', error)
                alert('保存中にエラーが発生しました: ' + error.message)
            }
        },
        async removeReservation(reservation) {
            this.reservation.delete_change_flag = "true"
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
        hhmmss2hhmm(value) {
            if (!value) return '';
            const [hours, minutes] = value.split(':');
            return `${hours}:${minutes}`;
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
            const date = new Date(value);
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            return `${hours}:${minutes}`;
        },
    }
}
</script>

<style scoped>
.details {
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: #ffffff;
  padding: 20px 5px;
  border-radius: 8px;
}

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

label {
    display: block;
    margin-bottom: 5px;
    color: #999;
}

select {
    width: 100%;
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.clickable {
  display: inline-flex;
  align-items: center;
  cursor: pointer; /* カーソルをポインターに変更 */
  color: #007bff; /* リンクのような色 */
}

.clickable:hover {
  color: #0056b3; /* ホバー時のテキスト色 */
}

.fas.fa-pen {
  margin-left: 5px; /* アイコンの左マージン */
  font-size: 0.9em; /* アイコンのサイズ */
  cursor: pointer; /* カーソルをポインターに変更 */
}
</style>
