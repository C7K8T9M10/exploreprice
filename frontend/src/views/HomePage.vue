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
        <el-menu-item index="/save">
          <i class="el-icon-star-off"></i>
          <span>查看保存商品</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-content">
      <el-header>
        <div class="search-container">
          <el-input
            v-model="searchQuery"
            placeholder="Search for products..."
            @input="searchProducts"
            clearable
          >
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
              <div class="product-name">{{ product.name }}</div>
              <div class="product-price">{{ product.price }}</div>
              <el-button type="primary" @click="saveProduct(product)">保存</el-button>
              <el-button type="info" @click="viewProductDetails(product)">查看详情</el-button>
              <el-button type="success" @click="viewPriceTrend(product)">查看价格走势</el-button>
            </li>
          </ul>
          <div v-else>No products found</div>
        </div>
      </el-main>
    </el-container>

    <el-dialog v-model="dialogVisible" title="商品详情">
      <div v-if="selectedProduct">
        <img :src="selectedProduct.image" alt="Product Image" />
        <div class="product-name">{{ selectedProduct.name }}</div>
        <div class="product-price">{{ selectedProduct.price }}</div>
        <div class="product-description">{{ selectedProduct.description }}</div>
        <div class="product-specifications">规格: {{ selectedProduct.specifications }}</div>
        <div class="product-fullname">全名: {{ selectedProduct.fullname }}</div>
        <div class="product-type">类型: {{ selectedProduct.type }}</div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
    <el-dialog v-model="priceTrendDialogVisible" title="价格走势">
      <div>
        <div ref="priceTrendChart" style="width: 100%; height: 400px"></div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="priceTrendDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </el-container>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

const searchQuery = ref('')
const products = ref([
  {
    id: 1,
    name: 'Test Product 1',
    price: '$10',
    image: 'https://via.placeholder.com/150',
    description: 'Description for Test Product 1',
    specifications: 'Spec 1',
    fullname: 'Test Product 1 Full Name',
    type: 'Type 1'
  },
  {
    id: 2,
    name: 'Test Product 2',
    price: '$20',
    image: 'https://via.placeholder.com/150',
    description: 'Description for Test Product 2',
    specifications: 'Spec 2',
    fullname: 'Test Product 2 Full Name',
    type: 'Type 2'
  },
  {
    id: 3,
    name: 'Test Product 3',
    price: '$30',
    image: 'https://via.placeholder.com/150',
    description: 'Description for Test Product 3',
    specifications: 'Spec 3',
    fullname: 'Test Product 3 Full Name',
    type: 'Type 3'
  }
])
const loading = ref(false)
const error = ref(null)
const dialogVisible = ref(false)
const selectedProduct = ref(null)
const priceTrendDialogVisible = ref(false)
const priceTrendChart = ref(null)

const searchProducts = async () => {
  if (searchQuery.value.trim() === '') {
    products.value = [
      {
        id: 1,
        name: 'Test Product 1',
        price: '$10',
        image: 'https://via.placeholder.com/150',
        description: 'Description for Test Product 1',
        specifications: 'Spec 1',
        barcode: '1234567890',
        fullname: 'Test Product 1 Full Name',
        type: 'Type 1'
      },
      {
        id: 2,
        name: 'Test Product 2',
        price: '$20',
        image: 'https://via.placeholder.com/150',
        description: 'Description for Test Product 2',
        specifications: 'Spec 2',
        barcode: '0987654321',
        fullname: 'Test Product 2 Full Name',
        type: 'Type 2'
      },
      {
        id: 3,
        name: 'Test Product 3',
        price: '$30',
        image: 'https://via.placeholder.com/150',
        description: 'Description for Test Product 3',
        specifications: 'Spec 3',
        barcode: '1122334455',
        fullname: 'Test Product 3 Full Name',
        type: 'Type 3'
      }
    ]
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await axios.post(`api/items/search/`, {
      keywords: searchQuery.value
    })
    if (response.status !== 200) {
      throw new Error('Failed to fetch products')
    }
    const contentType = response.headers['content-type']
    if (contentType && contentType.includes('application/json')) {
      products.value = response.data
      // Save the fetched data to SavedProduct
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

const saveProduct = (product) => {
  // Implement save product logic here
  console.log('Product saved:', product)
}
const viewPriceTrend = (product) => {
  priceTrendDialogVisible.value = true
  nextTick(() => {
    const chart = echarts.init(priceTrendChart.value)
    chart.setOption({
      title: {
        text: '价格走势'
      },
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: [820, 932, 901, 934, 1290, 1330, 1320],
          type: 'line'
        }
      ]
    })
  })
  console.log('View price trend:', product)
}
const viewProductDetails = (product) => {
  selectedProduct.value = product
  dialogVisible.value = true
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
  width: 200px;
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
</style>
