<!-- 提供側のトップ画面 -->
<!-- 顧客一覧、予約一覧へのリンクを含めたボタンの設置 -->
<template>
  <div>
    <div class="title">
      <h1>予約一覧</h1>
    </div>
    <table class="supplier-rsv">
      <tr>
        <th></th>
        <th>申込時間</th>
        <th>氏名</th>
        <th>内容</th>
        <th>予約日時</th>
        <th>承認</th>
      </tr>
      <tr>
        <td>
          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="reserve_detail"
          >
            詳細
          </button>
        </td>
        <td>2023/11/25 14:00</td>
        <td>鶴田悠也</td>
        <td>カット</td>
        <td>2023/11/27 14:00~15:00</td>
        <td>確定</td>
      </tr>
      <tr>
        <td>
          <button type="button" class="btn btn-outline-secondary">詳細</button>
        </td>
        <td>2023/11/25 14:00</td>
        <td>山田太郎</td>
        <td>パーマ</td>
        <td>2023/11/27 16:00~17:00</td>
        <td>確定</td>
      </tr>
      <tr>
        <td><button class="btn-details">詳細</button></td>
        <td>2023/11/25 14:00</td>
        <td>XXX</td>
        <td>ストレート・パーマ</td>
        <td>2023/11/29 14:00~15:00</td>
        <td>未承認</td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from 'axios'
// import Common from '@/plugins/common'

export default {
  // css: [
  //     '~/styles/reserve.css',
  // ],
  data() {
    return {
      accessToken: '',
      menulist: '',
    }
  },
  mounted() {
    //開発のためLIFFコメントアウト
    // this.$liffInit
    //   .then(() => {
    //     pass
    //   })
    //   .catch((error) => {
    //     this.liffError = error
    //   })
  },

  methods: {
    reserve() {
      this.$router.push('/reserving')
    },
    async getMenuList() {
      // ユーザのaccesstokenを取得
      try {
        const accessToken = liff.getAccessToken()
        return accessToken
      } catch (error) {
        console.error(error)
        return null
      }
    },
    async getAccessToken() {
      // ユーザのaccesstokenを取得
      try {
        const accessToken = liff.getAccessToken()
        return accessToken
      } catch (error) {
        console.error(error)
        return null
      }
    },
    async getUserProfile(accessToken) {
      // ユーザ情報を取得
      try {
        const response = await axios.get(`https://api.line.me/v2/profile`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        this.lineId = response.data.userId // 各種を更新
        this.displayName = response.data.displayName
        this.pictureUrl = response.data.pictureUrl
      } catch (error) {
        console.error(error)
      }
    },
    async getUserInfo() {
      const accessToken = await this.getAccessToken()
      if (accessToken) {
        await this.getUserProfile(accessToken)
      }
    },

    async sendData() {
      // sendDataメソッドを非同期関数に変更
      console.log('sendData started')
      await this.getUserInfo()
      console.log('getUserInfo completed')
      var apiurl =
        'https://4om5vxifil.execute-api.ap-northeast-1.amazonaws.com/rakujimu-1/RegistCustomerMst'
      var data = {
        id: 'test', // ask:自動採番だからいらない
        lineid: this.lineId,
        name: document.getElementById('name').value,
        date: document.getElementById('birthday').value, // ask:dynamo dateになっている
        address: document.getElementById('tel').value, // ask:telへ変更
        gender: document.getElementById('gender').value,
        mailaddress: document.getElementById('email').value,
      }
      console.log('data completed')
      var jsonData = JSON.stringify(data)
      try {
        const response = await axios.post(apiurl, jsonData, {
          headers: {
            'Content-Type': 'application/json',
          },
        })
        alert(response.data)
      } catch (error) {
        alert(error)
      }
    },

    reserve_detail() {
      this.$router.push('/supplier/reserve/reservedetail')
    },
  },
  // templateの選択
  layout: 'supplier',
}
</script>
