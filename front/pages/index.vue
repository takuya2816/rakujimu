<!-- LINEIDから顧客・提供者振り分けて各トップ画面へリダイレクト -->

<template>
  <div>
    <button @click="supplier">supplier</button>
    <button @click="customer">customer</button>
  </div>
</template>

<script>
// LINEIDから顧客・提供者振り分けて各トップ画面へリダイレクト
import axios from 'axios'
export default {
  methods: {
    customer() {
      this.$router.push('/customer')
    },
    supplier() {
      this.$router.push('/supplier')
    },
  },
  // templateの選択
  layout: 'customer',
}
</script>
