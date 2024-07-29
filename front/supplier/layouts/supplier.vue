<template>
  <div class="supplier-container">
    <Header />
    <div class="supplier-body">
      <Nuxt />
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '~/components/header.vue'
import Footer from '~/components/footer.vue'
export default {
  components: {
    Header,
    Footer,
  },
}
</script>

<style>
  .supplier-header {
    font-family: Arial, sans-serif;
  }

  .supplier-container {
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    background-color: #d9d9d9;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .supplier-body {
    font-family: Arial, sans-serif;
    margin-left: 3%;
    margin-right: 3%;
  } 

  /* 一覧表示用のcss */
  .list-body {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 70vh; /* スクロール可能な領域の高さを設定 */
    overflow-y: auto; /* 垂直スクロールを有効にする */
  }
  .list-header {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    border-bottom: 1px solid #ccc;
    position: sticky;
    top: 0;
    z-index: 1;
  }
  .list-header-item {
    flex-basis: 20%;
    text-align: center;
    font-weight: bold;
    color: #9B9A9A;
  }
  .list-content {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .list-record {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #fff;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  .list-info {
    display: flex;
    flex-grow: 1;
    justify-content: space-around;
    align-items: center;
  }

  .list-item {
    flex-basis: 20%;
    text-align: center;
  }
</style>