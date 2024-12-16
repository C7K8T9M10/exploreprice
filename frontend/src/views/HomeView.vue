<template>
  <header>
    <img
      alt="Vue logo"
      class="logo"
      src="@/assets/favicon.svg"
      width="250"
      height="175"
      style="display: block; margin-left: auto; margin-right: auto; text-align: center"
    />

    <div class="wrapper">
      <HelloWorld msg="欢迎来到价探网！" />

      <nav>
        <RouterLink to="/" class="nav-link" style="margin-left: 200px">登录</RouterLink>
        <RouterLink to="/register" class="nav-link" style="margin-left: 200px">注册</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />

  <div class="text">
    <h2>登录</h2>
    <p>登录享受完整服务</p>
    <form @submit.prevent="login">
      <div class="inputholder">
        <label for="username" style="width: 75px; text-align: left">用户名</label>
        <input
          type="text"
          id="username"
          class="input-field"
          name="username"
          v-model="username"
          required
        />
      </div>
      <div class="inputholder">
        <label for="password" style="width: 75px">密码</label>
        <input
          type="password"
          id="password1"
          class="input-field"
          name="password"
          v-model="password"
          required
        />
      </div>
      <button type="submit" class="submit-button">登录</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const response = await axios.post('api/catalog/login/', {
      username: username.value,
      password: password.value
    })

    if (response.status !== 200) {
      throw new Error('登录失败！请检查用户名密码是否正确！')
    }

    alert('登录成功')
    router.push({ path: '/home', query: { username: username.value } })
  } catch (error: any) {
    alert(error.message)
  }
}
</script>

<style>
/* 其他样式 */

.inputholder {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
  margin-left: 130px;
}

.input-field {
  width: 400px;
  height: 30px;
  margin-top: 5px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-button {
  background-color: aquamarine;
  color: black;
  height: 50px;
  text-align: center;
  width: 100px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #90ee90; /* 淡绿色，鼠标悬停时的视觉效果 */
}

.nav-link {
  margin-left: 20px;
  text-align: center;
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
  color: var(--color-text);
  text-decoration: none;
}

.nav-link:hover {
  background-color: #f0f0f0; /* 悬停时的背景色 */
}

.nav-link.router-link-exact-active {
  font-weight: bold;
  background-color: transparent;
}

/* 响应式设计 */
@media (min-width: 1024px) {
  .text {
    font-size: 1.2rem;
    text-align: center;
  }
  .inputholder {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 1rem;
  }
}

@media (max-width: 768px) {
  .logo {
    width: 150px;
    height: 100px;
    margin-left: 0;
  }

  .wrapper {
    text-align: center;
  }

  .nav-link {
    margin-left: 10px;
    padding: 0.5rem;
  }

  .inputholder {
    margin-left: 0;
    width: 100%;
  }

  .input-field {
    width: 90%;
  }

  .submit-button {
    width: 90%;
    margin: 0 auto;
  }
}
</style>
