<!-- 提供側のトップ画面 -->
<template>
  <div>
    <button
      type="button"
      class="btn btn-outline-secondary btn-lg"
      @click="GetCustomerList"
    >
      顧客一覧
    </button>
    <button
      type="button"
      class="btn btn-outline-secondary btn-lg"
      @click="GetReserveList"
    >
      予約一覧
    </button>
  </div>
</template>
<script>
// import Common from '@/plugins/common'

export default {
  // css: [
  //     '~/styles/supplier.css',
  // ],
  data() {
    return {
      accessToken: '',
      menulist: '',
    }
  },
  mounted() {
    // 開発のためLIFFコメントアウト
    // this.$liffInit
    //   .then(() => {
    //     pass
    //   })
    //   .catch((error) => {
    //     this.liffError = error
    //   })
  },

  methods: {
    GetCustomerList() {
      this.$router.push('/supplier/customerInfo')
    },
    GetReserveList() {
      this.$router.push('/supplier/reservedInfo')
    },
  },
  // templateの選択
  layout: 'supplier',
}
</script>
