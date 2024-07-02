<template>
  <div class="customer-container">
    <Header />
    <div class="customer-body">
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
  .customer-container {
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    background-color: #ffffff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  .customer-body {
    font-family: Arial, sans-serif;
    margin-left: 5%;
    margin-right: 5%;
  }

  input {
    border: 1px solid #ddd;
    border-radius: 5px;
    box-sizing: border-box;
    width: 100%;
    padding: 8px;
    margin-bottom: 6px;
    border: 1px solid #ccc;
    background-color: #d9d9d9;
    display: inline-block;
  }
  select {
    border: 1px solid #ddd;
    border-radius: 5px;
    box-sizing: border-box;
    width: 100%;
    padding: 8px;
    margin-bottom: 6px;
    border: 1px solid #ccc;
    background-color: #d9d9d9;
    display: inline-block;
  }
  button.send {
    background-color: #a19e9e;
    border-radius: 5px;
    color: white;
    padding: 14px 20px;
    margin: 40px 0;
    border: none;
    cursor: pointer;
    width: 100%;
  }
  button.btn-details {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0 auto;
    width: 100%;
    color: #333;
    font-size: 100%;
    font-weight: bold;
    background-color: #bbbbbb;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    border-radius: 6px;
    transition: 0.3s;
  }
</style>