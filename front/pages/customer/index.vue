<!-- 予約フォーム画面 -->
<template>
  <div>
    <div class="title">
      <h1>Contact</h1>
      <h3>予約フォーム</h3>
    </div>
    <div class="message">
      <p>
        XXXXXXの予約申込を行います<br />
        予約確定後に、店舗からご連絡申し上げます<br />
        ※送信時にサービス規約に同意したものとみなします
      </p>
    </div>
    <form class="contactForm">
      <div class="form-group">
        <label for="fullname">■お名前</label>
        <input type="text" id="fullname" v-model="fullname" required />
      </div>
      <div class="form-group">
        <label for="birthday">■生年月日</label>
        <input type="date" id="birthday" v-model="birthday" required />
      </div>
      <div class="form-group">
        <label for="gender">■性別</label>
        <select id="gender" v-model="gender" required>
          <option value="男性">男性</option>
          <option value="女性">女性</option>
          <option value="その他">その他</option>
        </select>
      </div>
      <div class="form-group">
        <label for="tel">■電話</label>
        <input type="tel" id="tel" v-model="tel" />
      </div>
      <div class="form-group">
        <label for="menu">■メニュー</label>
        <select id="menu" name="menu" required>
          <option v-for="item in menulist" :key="item.id" :value="item.name">
            {{ item.name }}
          </option>
        </select>
      </div>
      <button class="send" @click="reserve">日時選択へ</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import Common from '@/plugins/common'

export default {
  data() {
    return {
      menulist: [],
      fullname: '',
      birthday: '',
      gender: '',
      tel: '',
      menu: '',
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

    this.getMenuList()
  },

  methods: {
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
    async getMenuList() {
      // TODO: メニューリストを取得
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetServiceMst'
      const res = await Common.gateway_get(apiurl)
      this.menulist = res.Items
    },
    reserve() {
      this.$router.push('/customer/selectdate')
    },
  },
  // templateの選択
  layout: 'customer',
}
</script>
