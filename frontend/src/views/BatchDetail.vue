<template>
  <div class="batch-detail">
    <div v-if="loading" class="loading">Loading batch details...</div>
    
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="batch">
      <div class="header">
        <div>
          <h2>Batch #{{ batch.id }}</h2>
          <span :class="'badge badge-' + batch.status">{{ batch.status }}</span>
        </div>
        <router-link to="/batches" class="btn btn-secondary">← Back to Batches</router-link>
      </div>

      <div class="card batch-info">
        <h3>Batch Information</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Locale:</span>
            <span class="value">{{ batch.locale }}</span>
          </div>
          <div class="info-item">
            <span class="label">Created:</span>
            <span class="value">{{ formatDate(batch.created_at) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Started:</span>
            <span class="value">{{ formatDate(batch.started_at) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Completed:</span>
            <span class="value">{{ formatDate(batch.completed_at) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Total Articles:</span>
            <span class="value">{{ batch.total_articles }}</span>
          </div>
          <div class="info-item">
            <span class="label">Translated:</span>
            <span class="value">{{ batch.translated_articles }}</span>
          </div>
        </div>

        <div class="batch-progress" v-if="batch.total_articles > 0">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: (batch.translated_articles / batch.total_articles * 100) + '%' }"
            ></div>
          </div>
          <span class="progress-text">
            {{ Math.round(batch.translated_articles / batch.total_articles * 100) }}%
          </span>
        </div>
      </div>

      <div class="card">
        <div class="articles-header">
          <h3>Articles ({{ batch.articles.length }})</h3>
          <div class="search-box">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search articles..." 
              class="input"
            />
          </div>
        </div>

        <div class="articles-list">
          <div 
            v-for="article in filteredArticles" 
            :key="article.id" 
            class="article-item"
          >
            <div class="article-main">
              <div class="article-id">ID: {{ article.id }}</div>
              <div class="article-title">
                <strong>{{ article.title }}</strong>
                <span v-if="article.translation_status" :class="'badge badge-' + article.translation_status">
                  {{ article.translation_status }}
                </span>
              </div>
              <div class="article-preview">
                {{ getPreview(article.body) }}
              </div>
            </div>
            <div class="article-actions">
              <button 
                @click="viewArticle(article)" 
                class="btn btn-primary btn-sm"
              >
                View/Edit
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Article Viewer/Editor Modal -->
    <div v-if="selectedArticle" class="modal-overlay" @click="selectedArticle = null">
      <div class="modal modal-large" @click.stop>
        <div class="modal-header">
          <h3>Article #{{ selectedArticle.id }}</h3>
          <button @click="selectedArticle = null" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="comparison-view">
            <div class="comparison-column">
              <h4>Original</h4>
              <div class="article-content">
                <div class="content-section">
                  <label>Title:</label>
                  <div class="content-text">{{ originalArticle.title }}</div>
                </div>
                <div class="content-section">
                  <label>Body:</label>
                  <div class="content-html" v-html="originalArticle.body"></div>
                </div>
              </div>
            </div>
            <div class="comparison-column">
              <h4>Translation</h4>
              <div class="article-content">
                <div class="content-section">
                  <label>Title:</label>
                  <input 
                    v-model="selectedArticle.title" 
                    class="input"
                    @input="markAsEdited"
                  />
                </div>
                <div class="content-section">
                  <label>Body:</label>
                  <textarea 
                    v-model="selectedArticle.body" 
                    class="textarea"
                    @input="markAsEdited"
                  ></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="selectedArticle = null" class="btn btn-secondary">Close</button>
          <button 
            @click="saveArticle" 
            class="btn btn-success"
            :disabled="!isEdited || saving"
          >
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
  name: 'BatchDetail',
  data() {
    return {
      batch: null,
      loading: false,
      error: null,
      searchQuery: '',
      selectedArticle: null,
      originalArticle: null,
      isEdited: false,
      saving: false
    };
  },
  computed: {
    filteredArticles() {
      if (!this.batch || !this.batch.articles) return [];
      if (!this.searchQuery) return this.batch.articles;
      
      const query = this.searchQuery.toLowerCase();
      return this.batch.articles.filter(article => 
        article.title.toLowerCase().includes(query) ||
        article.id.toString().includes(query)
      );
    }
  },
  mounted() {
    this.loadBatch();
  },
  methods: {
    async loadBatch() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.getBatch(this.$route.params.id);
        this.batch = response.data.batch;
      } catch (err) {
        this.error = 'Failed to load batch: ' + err.message;
      } finally {
        this.loading = false;
      }
    },
    viewArticle(article) {
      this.selectedArticle = JSON.parse(JSON.stringify(article));
      this.originalArticle = JSON.parse(JSON.stringify(article));
      this.isEdited = false;
    },
    markAsEdited() {
      this.isEdited = true;
    },
    async saveArticle() {
      this.saving = true;
      this.error = null;
      try {
        await api.updateArticle(this.selectedArticle.id, {
          title: this.selectedArticle.title,
          body: this.selectedArticle.body
        });
        
        // Update the article in the batch
        const index = this.batch.articles.findIndex(a => a.id === this.selectedArticle.id);
        if (index !== -1) {
          this.batch.articles[index] = JSON.parse(JSON.stringify(this.selectedArticle));
        }
        
        this.selectedArticle = null;
        this.isEdited = false;
      } catch (err) {
        this.error = 'Failed to save article: ' + err.message;
      } finally {
        this.saving = false;
      }
    },
    getPreview(text) {
      if (!text) return '';
      const stripped = text.replace(/<[^>]*>/g, '');
      return stripped.length > 100 ? stripped.substring(0, 100) + '...' : stripped;
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString();
    }
  }
};
</script>

<style scoped>
.batch-detail {
  padding: 1rem 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.header h2 {
  margin-bottom: 0.5rem;
}

.batch-info {
  margin-bottom: 2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-item .label {
  font-weight: 500;
  color: #7f8c8d;
  font-size: 0.875rem;
}

.info-item .value {
  font-size: 1rem;
}

.batch-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.progress-bar {
  flex: 1;
  height: 12px;
  background-color: #ecf0f1;
  border-radius: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #3498db;
  transition: width 0.3s;
}

.progress-text {
  font-weight: 600;
  color: #3498db;
  min-width: 45px;
  text-align: right;
}

.articles-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.search-box {
  width: 300px;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.article-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.article-item:hover {
  background-color: #f8f9fa;
}

.article-main {
  flex: 1;
}

.article-id {
  font-size: 0.875rem;
  color: #7f8c8d;
  margin-bottom: 0.5rem;
}

.article-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.article-preview {
  color: #7f8c8d;
  font-size: 0.875rem;
}

.article-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  overflow-y: auto;
}

.modal-large {
  width: 95%;
  max-width: 1400px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-body {
  overflow-y: auto;
  flex: 1;
}

.comparison-view {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.comparison-column h4 {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #3498db;
}

.article-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.content-section label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.content-text {
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

.content-html {
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  border: 1px solid #e9ecef;
  max-height: 400px;
  overflow-y: auto;
}

.textarea {
  min-height: 400px;
}
</style>
