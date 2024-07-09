<!-- 予約完了画面 -->
<template>
  <div>
    <div class="title">
      <h2>予約が完了しました</h2>
    </div>
    <div class="message-under-title"></div>
    <div class="senddata">
      <div class="form-group">
        <p>お名前: {{ name }}</p>
      </div>
      <div class="form-group">
        <p>生年月日: {{ birthday }}</p>
      </div>
      <div class="form-group">
        <p>性別: {{ gender }}</p>
      </div>
      <div class="form-group">
        <p>電話: {{ tel }}</p>
      </div>
      <div class="form-group">
        <p>サービス: {{ serviceName }}</p>
      </div>
      <div class="form-group">
        <p>予約日時: {{ formatDatetime(reserveStDatetime) }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import common from '@/plugins/common'
export default {
  data() {
    return {
      name: this.$route.query.name,
      birthday: this.$route.query.birthday,
      gender: this.$route.query.gender,
      tel: this.$route.query.tel,
      serviceId: this.$route.query.serviceId,
      reserveStDatetime: this.$route.query.reserveStDatetime,
      serviceName: "",
    }
  },
  mounted() {
    this.getServiceList();
  },
  methods: {
    async getServiceList() {
      const apiurl =
        'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetServiceMst';
      const res = await common.gateway_get(apiurl);
      for (let service of res.Items) {
        if (service.id == this.serviceId) {
          this.serviceName = service.name;
        }
      };
    },
    formatDatetime(dateTimeStr){
      const [datePart, timePart] = dateTimeStr.split(' ');
      // 年月日を抽出してフォーマット
      const year = datePart.substring(0, 4);
      const month = datePart.substring(4, 6);
      const day = datePart.substring(6, 8);

      const formattedDate = `${year}-${month}-${day}`;
      const formattedDateTime = `${formattedDate} ${timePart}`;
      return formattedDateTime; 
    },
  },
  layout: 'customer',
}
</script>

<style>
.senddata {
  text-align: center;
}
</style>