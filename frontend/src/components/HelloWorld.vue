<script setup lang="ts">
defineProps<{
  msg: string
}>()
</script>

<template>
  <div class="greetings" role="region" aria-labelledby="greeting-heading">
    <h1 id="greeting-heading" class="green">{{ msg }}</h1>
    <h3>价探网是一个用于比较不同互联网电商平台价格的网站。</h3>
    <h3>
      我们使用的是来自不同平台的数据，然后将其进行比较。我们的服务宗旨是为了帮助用户找到最适合自己且价格最合理的商品！
    </h3>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box; /* 确保宽度包括内边距和边框 */
}

h1 {
  width: 400px;
  margin-left: 200px;
  font-weight: 500;
  font-size: 2.6rem;
  color: #4caf50; /* 绿色字体 */
  margin-bottom: 0.5rem; /* 添加一些底部边距 */
}

h3 {
  width: 400px;
  text-align: center;
  font-size: 1.2rem;
  color: #333; /* 深灰色字体 */
  margin-bottom: 1rem; /* 添加一些底部边距 */
  width: 100%; /* 确保段落宽度充满容器 */
}

.greetings {
  max-width: 800px; /* 限制最大宽度 */
  margin: 0 auto; /* 水平居中 */
  padding: 2rem; /* 四周添加一些内边距 */
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
