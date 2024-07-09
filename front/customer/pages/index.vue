<!-- 予約フォーム画面 -->
<template>
  <div>
    <div class="title">
      <h1>Contact</h1>
      <h3>予約フォーム</h3>
    </div>
    <div class="message-under-title">
      <p>
        XXXXXXの予約申込を行います<br />
        予約確定後に、店舗からご連絡申し上げます<br />
        ※送信時にサービス規約に同意したものとみなします
      </p>
    </div>
    <form class="contactForm" @submit.prevent="reserve">
      <div class="form-group">
        <label for="name">■お名前</label>
        <input type="text" id="name" v-model="name" required />
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
        <label for="service">■メニュー</label>
        <select id="service" v-model="serviceId" required>
          <option v-for="item in servicelist" :key="item.id" :value="item.id">
            {{ item.name }}
          </option>
        </select>
      </div>
      <button type="submit" class="send">日時選択へ</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import common from '@/plugins/common'

export default {
  data() {
    return {
      servicelist: [],
      name: '',
      birthday: '',
      gender: '',
      tel: '',
      serviceId: '',
    }
  },
  mounted() {
    // 開発のためliffコメントアウト
    this.$liffInit
      .then(() => {
        pass
      })
      .catch((error) => {
        this.liffError = error
      });
    this.getServiceList();
  },

  methods: {
    async getServiceList() {
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetServiceMst';
      const res = await common.gateway_get(apiurl);
      this.servicelist = res.Items;
    },
    reserve() {
      this.$router.push({path: '/selectdate/', 
                         query: {
                              name: this.name,
                              birthday: this.birthday,
                              gender: this.gender,
                              tel: this.tel,
                              serviceId: this.serviceId
                          }
                        });
    },
  },
  // templateの選択
  layout: 'customer',
}
</script>

<style>
.form-group {
  margin-bottom: 10px;
}
</style>