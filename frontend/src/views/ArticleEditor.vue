<template>
  <div class="article-editor">
    <div class="header">
      <h2>Article Editor</h2>
      <button @click="$router.back()" class="btn btn-secondary">← Back</button>
    </div>

    <div v-if="loading" class="loading">Loading article...</div>
    
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="article" class="editor-container">
      <div class="card">
        <h3>Translation Editor</h3>
        
        <div class="form-group">
          <label>Article ID</label>
          <input v-model="article.id" class="input" disabled />
        </div>

        <div class="form-group">
          <label>Title</label>
          <input v-model="article.title" class="input" />
        </div>

        <div class="form-group">
          <label>Body</label>
          <textarea v-model="article.body" class="textarea"></textarea>
        </div>

        <div class="form-actions">
          <button @click="$router.back()" class="btn btn-secondary">Cancel</button>
          <button @click="saveArticle" class="btn btn-success" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'ArticleEditor',
  data() {
    return {
      article: null,
      loading: false,
      saving: false,
      error: null
    };
  },
  mounted() {
    // This is a simplified version - in a real app, you'd load the article
    // For now, it's primarily accessed through BatchDetail modal
    this.article = {
      id: this.$route.params.id,
      title: '',
      body: ''
    };
  },
  methods: {
    async saveArticle() {
      this.saving = true;
      this.error = null;
      try {
        await api.updateArticle(this.article.id, {
          title: this.article.title,
          body: this.article.body
        });
        this.$router.back();
      } catch (err) {
        this.error = 'Failed to save article: ' + err.message;
      } finally {
        this.saving = false;
      }
    }
  }
};
</script>

<style scoped>
.article-editor {
  padding: 1rem 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.editor-container {
  max-width: 800px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}
</style>
