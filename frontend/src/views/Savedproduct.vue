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
        <el-menu-item :index="`/home?username=${username}`">
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
      <el-main>
        <el-header>每小时刷新一次商品价格，降价会弹出通知提醒</el-header>
        <el-table :data="savedProducts" v-loading="loading">
          <el-table-column prop="name" label="商品名称"></el-table-column>
          <el-table-column prop="price" label="价格"></el-table-column>
          <el-table-column label="操作">
            <template v-slot="scope">
              <el-button @click="fetchLatestPrice(scope.row)" type="primary" plain>
                获取最新价格
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      savedProducts: [],
      username: '',
      loading: false
    }
  },
  methods: {
    async fetchSavedProductsFromAPI() {
      this.loading = true
      try {
        const response = await axios.post('/api/items/getsav/', { username: this.username })
        if (response.status !== 200) {
          throw new Error('Network response was not ok')
        }
        const data = response.data
        this.savedProducts = data.map((item) => ({
          name: item.name,
          price: item.latest_price,
          link: item.link
        }))
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error)
      } finally {
        this.loading = false
      }
    },
    async fetchLatestPrice(product) {
      this.loading = true
      const formerprice = product.price
      try {
        const response = await axios.post('/api/items/getprice/', { name: product.name })
        if (response.status !== 200) {
          throw new Error('Network response was not ok')
        }
        const data = response.data
        product.price = data.latest_price
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error)
      } finally {
        this.loading = false
      }
      if (formerprice > product.price) {
        this.$notify({
          title: '降价通知',
          message: `${product.name} 降价啦！现价 ${product.price}`,
          type: 'success'
        })
      }
    },
    checkLogin() {
      const urlParams = new URLSearchParams(window.location.search)
      this.username = urlParams.get('username')
      if (!this.username) {
        this.$router.push('/')
      }
    }
  },
  async fetchLatestPrices() {
    this.loading = true
    try {
      for (const product of this.savedProducts) {
        await this.fetchLatestPrice(product)
      }
    } catch (error) {
      console.error('There was a problem with fetching the latest prices:', error)
    } finally {
      this.loading = false
    }
  },
  mounted() {
    this.checkLogin()
    this.fetchSavedProductsFromAPI()
    // Set an interval to fetch the latest prices periodically
    setInterval(this.fetchLatestPrices, 3600000) // Fetch every 3600 seconds (1 hour)
  }
}
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  margin: 0 auto;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: 'Arial', sans-serif;
}

.aside {
  background-color: #333;
  width: 100%;
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

.header {
  display: flex;
  justify-content: flex-center;
  align-items: center;
  padding: 6px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
  flex-wrap: wrap;
}

@media (min-width: 768px) {
  .home-page {
    flex-direction: row;
  }

  .aside {
    width: 200px;
  }

  .main-content {
    flex: 1;
  }
}
</style>
