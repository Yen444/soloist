<template>
  <div id="app">
    <basic-vue-chat 
      :new-message="message" 
      :initial-feed="initialFeed"
      />
  </div>
</template>

<script>
import BasicVueChat from "./components/basic-vue-chat/BasicVueChat.vue";

export default {
  name: "App",
  components: {
    BasicVueChat
  },
  data: function() {
    return {
      message: {},
      initialFeed: [
        {
          id: 1,
          author: "Person",
          imageUrl: "http://path/to/image",
          contents: "hi there",
          date: "16:30"
        },
        {
          id: 0,
          author: "Me",
          contents: "hello",
          date: "16:30"
        }
      ]
    };
  }
};
</script>

<style lang="scss">
</style>
