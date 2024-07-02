<!-- 予約完了画面 -->
<template>
  <div>
    <div class="title">
      <h2>予約が完了しました</h2>
    </div>
    <div class="message-under-title"></div>
    <div class="senddata">
      <div class="form-group">
        <p>お名前</p>
      </div>
      <div class="form-group">
        <p>生年月日</p>
      </div>
      <div class="form-group">
        <p>性別</p>
      </div>
      <div class="form-group">
        <p>電話</p>
      </div>
      <div class="form-group">
        <p>メールアドレス</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // templateの選択
  layout: 'customer',
}
</script>

<style>
.senddata {
  text-align: center;
}
</style>