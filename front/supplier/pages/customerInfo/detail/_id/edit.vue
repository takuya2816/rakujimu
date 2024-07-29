<template>
    <div>
        <div class="title">
            <h1>顧客情報編集</h1>
        </div>
        <div class="details">
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
        <div class="buttons">
            <button class="cancel-button" @click="cancelEdit">キャンセル</button>
            <button class="post-button" @click="saveCustomerInfo">保存</button>
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
        // 開発のためliffコメントアウト
        // this.$liffInit
        //   .then(() => {
        //     this.idToken = liff.getIDToken();
        //   })
        //   .catch((error) => {
        //     this.liffError = error
        //   }),
        this.getCustomerMst(this.$route.params.id)
    },
    methods: {
        async getCustomerMst(customerId) {
            const apiurl =
                'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetCustomerMst'
            const data = { customer_id: [customerId] }
            const res = await common.gateway_get(apiurl, data)
            this.customer = res[0]
        },
        async saveCustomerInfo() {
            try {
                const apiurl = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistCustomerMst'
                const res = await common.gateway_post(apiurl, this.customer)
                if (res && res.result === "ok") {
                    // 成功時の処理
                    this.$router.push(`/customerInfo/detail/${this.$route.params.id}`)
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
            this.$router.push(`/customerInfo/detail/${this.$route.params.id}`)
        }
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
    align-items: center;
    margin-top: 10px;
    margin-bottom: 10px;
}

.detail-item .label {
    color: #999;
    flex-basis: 30%;
    text-align: right;
    margin-right: 10px;
}

.detail-item .value {
    color: #333;
    flex-basis: 70%;
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

.list-record:hover {
  background-color: #f0f0f0; /* 背景色を変更 */
  /* box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* ボックスシャドウを追加 */
  /* border: 4px solid #ccc; /* ボーダーを追加 */
}
</style>