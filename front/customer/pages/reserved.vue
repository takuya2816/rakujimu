<template>
  <div>
    <div class="title">
      <h2>予約が完了しました</h2>
    </div>
    <div class="message-under-title">ご予約ありがとうございます。<br>変更の際はお電話にてご連絡ください。</div>
    <div class="senddata">
      <div class="form-group">
        <div class="label">お名前:</div>
        <div class="value">{{ name }}</div>
      </div>
      <div class="form-group">
        <div class="label">生年月日:</div>
        <div class="value">{{ birthday }}</div>
      </div>
      <div class="form-group">
        <div class="label">性別:</div>
        <div class="value">{{ gender }}</div>
      </div>
      <div class="form-group">
        <div class="label">電話:</div>
        <div class="value">{{ tel }}</div>
      </div>
      <div class="form-group">
        <div class="label">サービス:</div>
        <div class="value">{{ serviceName }}</div>
      </div>
      <div class="form-group">
        <div class="label">予約日時:</div>
        <div class="value">{{ formatDatetime(reserveStDatetime) }}</div>
      </div>
    </div>
  </div>
</template>


<script>
import common from '@/plugins/common'
export default {
  data() {
    console.log(this.$route.query);
    return {
      name: this.$route.query.name,
      birthday: this.$route.query.birthday,
      gender: this.$route.query.gender,
      tel: this.$route.query.tel,
      serviceId: this.$route.query.service_id,
      reserveStDatetime: this.$route.query.reserve_st_datetime,
      serviceName: "",
    }
  },
  mounted() {
    this.getServiceList();
    console.log(this.gender);
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
.title {
  text-align: center;
  margin-bottom: 20px;
}

.message-under-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.0em;
  color: #666;
}

.senddata {
  padding: 5px;
  border-radius: 8px;
  margin: 5px 0;
}

.form-group {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  background-color: #fff; /* 文字部分の背景色を白に設定 */
  padding: 10px;
  border-radius: 4px;
}

.label {
  flex-basis: 40%;
  text-align: right;
  margin-right: 20px;
  font-weight: bold;
  color: #333;
  font-size: 1.1em; /* 文字を少し大きく */
}

.value {
  flex-basis: 60%;
  text-align: left;
  color: #333;
  font-size: 1.1em; /* 文字を少し大きく */
}

</style>