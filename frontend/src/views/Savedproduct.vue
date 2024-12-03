<template>
  <el-container class="home-page">
    <!-- 侧边栏 -->
    <el-aside class="aside" width="200px">
      <el-menu
        default-active="2"
        class="el-menu-vertical-demo"
        background-color="#333"
        text-color="#fff"
        active-text-color="#ffd04b"
        :router="true"
      >
        <el-menu-item index="/home">
          <i class="el-icon-search"></i>
          <span>搜索商品</span>
        </el-menu-item>
        <el-menu-item index="/save">
          <i class="el-icon-star-off"></i>
          <span>查看保存商品</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-content">
      <el-header>
        <el-button type="primary" @click="fetchLatestPrices">手动刷新价格</el-button>
      </el-header>
      <el-main>
        <el-table :data="savedProducts">
          <el-table-column prop="name" label="商品名称"></el-table-column>
          <el-table-column prop="price" label="价格"></el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      savedProducts: []
    }
  },
  methods: {
    fetchSavedProducts() {
      // Fetch saved products from an API or local storage
      // This is just a placeholder example
      this.savedProducts = [
        { name: '商品1', price: 100 },
        { name: '商品2', price: 200 }
      ]
    },
    fetchLatestPrices() {
      // Fetch the latest prices for the saved products
      // This is just a placeholder example
      this.savedProducts = this.savedProducts.map((product) => {
        return {
          ...product,
          price: product.price + Math.floor(Math.random() * 10) // Simulate price update
        }
      })
    }
  },
  mounted() {
    this.fetchSavedProducts()
    // Set an interval to fetch the latest prices periodically
    setInterval(this.fetchLatestPrices, 60000) // Fetch every 60 seconds
  }
}
</script>

<style scoped>
.home-page {
  display: flex;
  height: 100vh; /* Adjusted to occupy 100% of the viewport height */
  width: 80vw; /* Adjusted to occupy 80% of the viewport width */
  margin: 0 auto; /* Center the container horizontally */
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: 'Arial', sans-serif;
}

.aside {
  background-color: #333;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
