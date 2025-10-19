<template>
  <div class="layout">
    <Header />
    <main class="content">
      <h2>Contenido del cuerpo</h2>
      <p>El layout mantiene el header y footer fijos.</p>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.content {
  flex: 1;
  padding: 2rem;
  text-align: center;
}
</style>
