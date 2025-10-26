import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  // Health check
  healthCheck() {
    return api.get('/health');
  },

  // Configuration
  getConfig() {
    return api.get('/config');
  },

  // Glossary
  getGlossary() {
    return api.get('/glossary');
  },

  addGlossaryTerm(source, target) {
    return api.post('/glossary', { source, target });
  },

  // Batches
  listBatches() {
    return api.get('/batches');
  },

  createBatch(locale = 'en-us') {
    return api.post('/batches', { locale });
  },

  getBatch(batchId) {
    return api.get(`/batches/${batchId}`);
  },

  startBatch(batchId) {
    return api.post(`/batches/${batchId}/start`);
  },

  // Articles
  translateArticle(articleId, article) {
    return api.post(`/articles/${articleId}/translate`, { article });
  },

  updateArticle(articleId, data) {
    return api.put(`/articles/${articleId}`, data);
  },

  // Output files
  listOutputFiles() {
    return api.get('/output/list');
  },

  getOutputFile(filename) {
    return api.get(`/output/${filename}`);
  }
};
