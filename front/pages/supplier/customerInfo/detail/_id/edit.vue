<template>
    <div>
        <div class="title">
            <h1>顧客情報編集</h1>
        </div>
        <div class="customer-edit">
            <div class="profile">
                <div class="profile-info">
                    <div class="detail-item">
                        <span class="label">氏名</span>
                        <input v-model="customer.name" class="value" type="text">
                    </div>
                    <div class="detail-item">
                        <span class="label">性別</span>
                        <select v-model="customer.gender" class="value">
                            <option value="男性">男性</option>
                            <option value="女性">女性</option>
                            <option value="その他">その他</option>
                        </select>
                    </div>
                    <div class="detail-item">
                        <span class="label">生年月日</span>
                        <input v-model="customer.birthday" class="value" type="date">
                    </div>
                    <div class="detail-item">
                        <span class="label">電話</span>
                        <input v-model="customer.tel" class="value" type="tel">
                    </div>
                </div>
            </div>
        </div>
        <div class="buttons">
            <button class="save-button" @click="saveCustomerInfo">保存</button>
            <button class="cancel-button" @click="cancelEdit">キャンセル</button>
        </div>
    </div>
</template>

<script>
import common from '@/plugins/common'
export default {
    layout: 'supplier',
    data() {
        return {
            customer: {}
        }
    },
    mounted() {
        this.getCustomerMst(this.$route.params.id)
    },
    methods: {
        async getCustomerMst(customerId) {
            const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetCustomerMst'
            const data = { customerId }
            const res = await common.gateway_get(apiurl, data)
            this.customer = res
        },
        async saveCustomerInfo() {
            try {
                console.log(this.customer)
                const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistCustomerMst'
                const res = await common.gateway_post(apiurl, this.customer)
                if (res && res.result === "ok") {  // 厳密等価演算子を使用し、resが存在することを確認
                    // 成功時の処理
                    this.$router.push(`/supplier/customerInfo/detail/${this.$route.params.id}`)
                } else {
                    // レスポンスが期待通りでない場合の処理
                    console.error('Unexpected response:', res)
                    alert('保存に失敗しました。予期せぬレスポンスを受け取りました。')
                }
            } catch (error) {
                // エラーハンドリング
                console.error('Error saving customer info:', error)
                alert('保存中にエラーが発生しました。')
            }
        },
        cancelEdit() {
            this.$router.push(`/supplier/customerInfo/detail/${this.$route.params.id}`)
        }
    }
}
</script>

<style scoped>
.customer-edit {
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
}

.detail-item .label {
    color: #999;
    flex-basis: 40%;
    text-align: right;
    margin-right: 20px;
}

.detail-item .value {
    color: #333;
    flex-basis: 60%;
    text-align: left;
}

input,
select {
    width: 100%;
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.buttons {
    margin-top: 20px;
    display: flex;
    justify-content: center;
}

.save-button,
.cancel-button {
    padding: 10px 20px;
    margin: 0 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
</style>