<template>
  <header>
    <img
      alt="Vue logo"
      class="logo"
      src="@/assets/favicon.svg"
      width="250"
      height="175"
      style="margin-left: 290px"
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
    <h2>注册</h2>
    <p>请填写以下信息进行注册</p>
    <form @submit.prevent="register">
      <div class="inputholder">
        <label for="email" style="width: 100px">邮箱</label>
        <input type="email" id="email" class="input-field" name="email" required v-model="email" />
      </div>
      <div class="inputholder">
        <label for="username" style="width: 100px">用户名</label>
        <input
          type="text"
          id="username"
          class="input-field"
          name="username"
          required
          v-model="username"
        />
      </div>
      <div class="inputholder">
        <label for="password" style="width: 100px">密码</label>
        <input
          type="password"
          id="password"
          class="input-field"
          name="password"
          required
          v-model="password"
        />
      </div>
      <div class="inputholder">
        <label for="confirm_password" style="width: 100px">确认密码</label>
        <input
          type="password"
          id="confirm_password"
          class="input-field"
          name="confirm_password"
          required
          v-model="confirmPassword"
        />
      </div>
      <button type="submit" class="submit-button">注册</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')

const router = useRouter()

const register = async () => {
  if (password.value.length < 6) {
    alert('密码必须至少6位')
    return
  }

  if (password.value !== confirmPassword.value) {
    alert('密码和确认密码不匹配')
    return
  }

  try {
    const response = await axios.post('api/catalog/register/', {
      email: email.value,
      username: username.value,
      password: password.value
    })

    if (response.status !== 201) {
      throw new Error('注册失败，用户名或邮箱已存在!')
    }

    alert('注册成功')
    router.push('/')
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
</style>
