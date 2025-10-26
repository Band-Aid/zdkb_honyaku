<template>
  <div class="article-list">
    <div class="header">
      <h2>Translation Articles</h2>
      <div class="header-actions">
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search articles..." 
            class="input"
          />
        </div>
        <button @click="$router.push('/glossary')" class="btn btn-secondary">
          Manage Glossary
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading articles...</div>
    
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="!loading && articles.length === 0" class="info">
      No articles found. Articles will appear here when batches are created.
    </div>

    <div class="articles-table" v-if="!loading && articles.length > 0">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Batch</th>
            <th>Status</th>
            <th>Locale</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="article in filteredArticles" 
            :key="article.id"
            class="article-row"
          >
            <td class="article-id">{{ article.id }}</td>
            <td class="article-title">
              <div class="title-text">{{ article.title }}</div>
              <div class="preview-text">{{ getPreview(article.body) }}</div>
            </td>
            <td class="batch-info">
              <router-link :to="`/batches/${article.batchId}`" class="batch-link">
                Batch #{{ article.batchId }}
              </router-link>
            </td>
            <td>
              <span 
                v-if="article.translation_status" 
                :class="'badge badge-' + article.translation_status"
              >
                {{ article.translation_status }}
              </span>
              <span v-else class="badge badge-pending">pending</span>
            </td>
            <td>{{ article.locale || 'N/A' }}</td>
            <td>{{ formatDate(article.created_at) }}</td>
            <td>
              <button 
                @click="viewArticle(article)" 
                class="btn btn-primary btn-sm"
              >
                View/Edit
              </button>
            </td>
          </tr>
        </tbody>
      </table>
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
  name: 'ArticleList',
  data() {
    return {
      articles: [],
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
      if (!this.searchQuery) return this.articles;
      
      const query = this.searchQuery.toLowerCase();
      return this.articles.filter(article => 
        article.title.toLowerCase().includes(query) ||
        article.id.toString().includes(query) ||
        (article.body && article.body.toLowerCase().includes(query))
      );
    }
  },
  mounted() {
    this.loadArticles();
  },
  methods: {
    async loadArticles() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.listBatches();
        const batches = response.data.batches;
        
        // Flatten all articles from all batches
        this.articles = [];
        batches.forEach(batch => {
          if (batch.articles && batch.articles.length > 0) {
            batch.articles.forEach(article => {
              this.articles.push({
                ...article,
                batchId: batch.id,
                batchLocale: batch.locale,
                batchStatus: batch.status
              });
            });
          }
        });
        
        // Sort by creation date, newest first
        this.articles.sort((a, b) => {
          const dateA = new Date(a.created_at || 0);
          const dateB = new Date(b.created_at || 0);
          return dateB - dateA;
        });
      } catch (err) {
        this.error = 'Failed to load articles: ' + err.message;
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
        
        // Update the article in the list
        const index = this.articles.findIndex(a => a.id === this.selectedArticle.id);
        if (index !== -1) {
          this.articles[index] = JSON.parse(JSON.stringify(this.selectedArticle));
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
      // Remove all HTML tags to prevent XSS - this is for text preview only
      // The regex removes tags completely, preventing any XSS attacks
      const stripped = text.replace(/<[^>]*>/g, '');
      return stripped.length > 100 ? stripped.substring(0, 100) + '...' : stripped;
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    }
  }
};
</script>

<style scoped>
.article-list {
  padding: 1rem 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-box {
  width: 300px;
}

.articles-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #f8f9fa;
  border-bottom: 2px solid #e9ecef;
}

th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
}

tbody tr {
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

tbody tr:hover {
  background-color: #f8f9fa;
}

td {
  padding: 1rem;
}

.article-id {
  color: #7f8c8d;
  font-family: monospace;
}

.article-title {
  max-width: 400px;
}

.title-text {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.preview-text {
  font-size: 0.875rem;
  color: #7f8c8d;
}

.batch-link {
  color: #3498db;
  text-decoration: none;
}

.batch-link:hover {
  text-decoration: underline;
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

.modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.modal-large {
  width: 95%;
  max-width: 1400px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #7f8c8d;
  line-height: 1;
}

.close-btn:hover {
  color: #2c3e50;
}

.modal-body {
  overflow-y: auto;
  flex: 1;
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
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
