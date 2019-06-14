<template>
  <div class="auth-view">
    <div class="auth-form">
      <h1>ci-hub</h1>
      <label for="username" id="username-label">username:</label>
      <input type="text" name="username" v-model="usernameAuth" @keyup.enter="send">
      <label for="password" id="password-label">password:</label>
      <input type="password" name="password" v-model="passwordAuth" @keyup.enter="send">
      <button @click="send">Log In</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthView',
  data() {
    return {
      usernameAuth: '',
      passwordAuth: ''
    }
  },
  methods: {
    send() {
      this.$backend.authenticate(this.usernameAuth, this.passwordAuth).then(() => {
        this.$http.defaults.headers
          .common['Authorization'] = `Basic ${btoa(`${this.usernameAuth}:${this.passwordAuth}`)}`;
        this.$emit('loggedIn', true);
      }).catch(() => {
        this.$emit('loggedIn', false);
      });
    }
  }
}
</script>

<style scoped>
.auth-view {
  display: flex;
  justify-content: center;
  align-content: center;
  height: 100vh;
  align-items: center;
}
.auth-view h1 {
  font-family: "SourceSansSemi";
  font-size: 2.8rem;
  text-align: center;
}
.auth-form {
  display: flex;
  flex-direction: column;
}
</style>