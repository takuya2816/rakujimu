<!-- 提供側のトップ画面 -->
<template>
  <div>
    <button @click="$router.push('/supplier/customer/customerlist')">
      顧客一覧
    </button>
    <NuxtLink to="/supplier/reserve/reservelist">予約一覧</NuxtLink>
  </div>
</template>
<script>
// LINEIDから顧客・提供者振り分けて各トップ画面へリダイレクト
export default {
  // templateの選択
  layout: 'supplier',
}
</script>
