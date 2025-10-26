import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import BatchList from './views/BatchList.vue';
import BatchDetail from './views/BatchDetail.vue';
import ArticleEditor from './views/ArticleEditor.vue';
import GlossaryManager from './views/GlossaryManager.vue';

const routes = [
  { path: '/', redirect: '/batches' },
  { path: '/batches', component: BatchList },
  { path: '/batches/:id', component: BatchDetail },
  { path: '/articles/:id/edit', component: ArticleEditor },
  { path: '/glossary', component: GlossaryManager }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');
