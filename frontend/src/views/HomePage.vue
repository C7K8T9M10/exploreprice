<template>
  <el-container class="home-page">
    <!-- 侧边栏 -->
    <el-aside class="aside" width="200px">
      <el-menu
        default-active="1"
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
        <el-menu-item index="/save" @click="navigateToSavedProducts">
          <i class="el-icon-star-off"></i>
          <span>查看保存商品</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-content">
      <el-header>
        <div class="search-container">
          <el-input v-model="searchQuery" placeholder="Search for products..." clearable>
            <template #append>
              <el-button icon="el-icon-search" @click="searchProducts">搜索</el-button>
            </template>
          </el-input>
        </div>
      </el-header>

      <el-main>
        <div class="results-container">
          <div v-if="loading">Loading...</div>
          <div v-if="error">{{ error }}</div>
          <ul v-if="products.length">
            <li v-for="product in products" :key="product.id">
              <img :src="product.image" alt="Product Image" />
              <div class="product-name">
                {{
                  product.name.length > 30 ? product.name.substring(0, 30) + '...' : product.name
                }}
              </div>
              <div class="product-price">{{ product.price }}</div>
              <el-button type="primary" @click="saveProduct(product)">保存</el-button>
              <el-button type="info" @click="viewProductDetails(product)">查看详情</el-button>
              <el-button type="success" @click="viewProductLink(product)">进入商品链接</el-button>
              <el-button type="warning" @click="viewPriceTrend(product)">查看价格走势</el-button>
            </li>
          </ul>
          <div v-else>No products found</div>
        </div>
      </el-main>
    </el-container>

    <el-dialog v-model="dialogVisible" title="商品详情">
      <div v-if="selectedProduct">
        <img :src="selectedProduct.image" alt="Product Image" />
        <div class="product-price">当前售价：{{ selectedProduct.price }}</div>
        <div class="product-link">商品链接：{{ selectedProduct.link }}</div>
        <div class="product-specifications">规格: {{ selectedProduct.specifications }}</div>
        <div class="product-fullname">全名: {{ selectedProduct.name }}</div>
        <div class="product-type">类型: {{ selectedProduct.type }}</div>
        <div class="product-type">类型: {{ selectedProduct.type }}</div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
    <el-dialog v-model="priceTrendDialogVisible" title="价格走势">
      <div>
        <img
          v-if="selectedProduct && selectedProduct.priceChartUrl"
          :src="selectedProduct.priceChartUrl"
          alt="Price Trend Chart"
          style="width: 100%"
        />
        <p>{{ selectedProduct.priceChartUrl }}</p>
        <p>价格走势图</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="priceTrendDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </el-container>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
import { el } from 'element-plus/es/locales.mjs'

const searchQuery = ref('')
const products = ref([])
const loading = ref(false)
const error = ref(null)
const dialogVisible = ref(false)
const selectedProduct = ref(null)
const priceTrendDialogVisible = ref(false)

const searchProducts = async () => {
  if (searchQuery.value.trim() === '') {
    products.value = []
    return
  }

  loading.value = true
  error.value = null
  try {
    const response = await axios.get(`/api/items/search/`, {
      params: {
        keywords: searchQuery.value.split(' ')
      }
    })
    if (response.status !== 200) {
      throw new Error('Failed to fetch products')
    }
    const contentType = response.headers['content-type']
    if (contentType && contentType.includes('application/json')) {
      products.value = response.data
      localStorage.setItem('SavedProduct', JSON.stringify(response.data))
    } else {
      throw new Error('Invalid content type')
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const viewProductLink = (product) => {
  window.open(product.link)
}
onMounted(async () => {
  try {
    const response = await axios.get('api/items/rand')
    if (response.status === 200) {
      products.value = response.data
    } else {
      throw new Error('Failed to fetch random products')
    }
  } catch (err) {
    error.value = err.message
  }
})

const saveProduct = async (product) => {
  try {
    console.log('Button clicked')
    const urlParams = new URLSearchParams(window.location.search)
    const response = await axios.post('/api/items/save/', {
      item_name: product.name,
      user_name: urlParams.get('username')
    })
    if (response.status === 200) {
      console.log('Item saved successfully')
    } else {
      console.error('Failed to save item')
    }
  } catch (error) {
    console.error('Error saving item:', error)
  }
}
const viewPriceTrend = async (product) => {
  try {
    const response = await axios.post('/api/items/getimg/', {
      link: product.link
    })
    if (response.status === 200) {
      const myid = response.data.item_id
      const priceChartUrl = response.data.price_chart
      selectedProduct.value = { ...product, priceChartUrl }
      priceTrendDialogVisible.value = true
    }
  } catch (error) {
    console.error('Error fetching price trend:', error)
  }
}
const navigateToSavedProducts = () => {
  const urlParams = new URLSearchParams(window.location.search)
  const username = urlParams.get('username')
  window.location.href = `/save?username=${username}`
}
const viewProductDetails = (product) => {
  selectedProduct.value = product
  dialogVisible.value = true
}

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  const username = urlParams.get('username')
  if (!username) {
    alert('用户未登录')
    window.location.href = '/'
  }
})
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

.el-header {
  padding: 0;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.el-main {
  flex: 1;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.search-container .el-input {
  width: 100%;
  max-width: 400px;
}

.results-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.results-container ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.results-container li {
  width: 100%;
  max-width: 200px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.results-container li img {
  width: 100%;
  height: 150px;
  background-color: #f0f0f0;
  margin-bottom: 10px;
}

.results-container li .product-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

.results-container li .product-price {
  color: #e74c3c;
  font-size: 18px;
  font-weight: bold;
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
