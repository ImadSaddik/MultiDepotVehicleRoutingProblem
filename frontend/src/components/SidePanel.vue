<template>
  <div class="container">Hi, I'm a side panel!</div>
</template>

<script>
export default {
  name: "SidePanel",
  data() {
    return {};
  },
};
</script>

<style scoped>
.container {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 20rem;
  background-color: rgba(255, 255, 255, 0.95);
  border-left: 1px solid #adadad;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  overflow-y: auto;
  padding: 1rem;
}
</style>
