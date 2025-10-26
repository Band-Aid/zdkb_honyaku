<template>
  <div class="batch-list">
    <div class="header">
      <h2>Translation Batches</h2>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + New Batch
      </button>
    </div>

    <div v-if="loading" class="loading">Loading batches...</div>
    
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="!loading && batches.length === 0" class="info">
      No batches found. Create a new batch to get started.
    </div>

    <div class="batch-grid">
      <div v-for="batch in batches" :key="batch.id" class="card batch-card">
        <div class="batch-header">
          <h3>Batch #{{ batch.id }}</h3>
          <span :class="'badge badge-' + batch.status">{{ batch.status }}</span>
        </div>
        
        <div class="batch-details">
          <div class="detail-row">
            <span class="label">Locale:</span>
            <span class="value">{{ batch.locale }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Created:</span>
            <span class="value">{{ formatDate(batch.created_at) }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Articles:</span>
            <span class="value">{{ batch.translated_articles }} / {{ batch.total_articles }}</span>
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

        <div class="batch-actions">
          <button 
            v-if="batch.status === 'pending'" 
            @click="startBatch(batch.id)" 
            class="btn btn-success"
            :disabled="processing"
          >
            Start Translation
          </button>
          <router-link 
            :to="`/batches/${batch.id}`" 
            class="btn btn-primary"
          >
            View Details
          </router-link>
        </div>
      </div>
    </div>

    <!-- Create Batch Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Create New Batch</h3>
          <button @click="showCreateModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Source Locale</label>
            <select v-model="newBatchLocale" class="input">
              <option value="en-us">English (US)</option>
              <option value="en-gb">English (UK)</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCreateModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="createBatch" class="btn btn-primary" :disabled="creating">
            {{ creating ? 'Creating...' : 'Create Batch' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'BatchList',
  data() {
    return {
      batches: [],
      loading: false,
      error: null,
      showCreateModal: false,
      newBatchLocale: 'en-us',
      creating: false,
      processing: false
    };
  },
  mounted() {
    this.loadBatches();
  },
  methods: {
    async loadBatches() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.listBatches();
        this.batches = response.data.batches;
      } catch (err) {
        this.error = 'Failed to load batches: ' + err.message;
      } finally {
        this.loading = false;
      }
    },
    async createBatch() {
      this.creating = true;
      this.error = null;
      try {
        await api.createBatch(this.newBatchLocale);
        this.showCreateModal = false;
        this.newBatchLocale = 'en-us';
        await this.loadBatches();
      } catch (err) {
        this.error = 'Failed to create batch: ' + err.message;
      } finally {
        this.creating = false;
      }
    },
    async startBatch(batchId) {
      if (!confirm('Start translating this batch? This may take some time.')) {
        return;
      }
      
      this.processing = true;
      this.error = null;
      try {
        await api.startBatch(batchId);
        await this.loadBatches();
      } catch (err) {
        this.error = 'Failed to start batch: ' + err.message;
      } finally {
        this.processing = false;
      }
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
.batch-list {
  padding: 1rem 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.batch-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.batch-card {
  transition: transform 0.2s;
}

.batch-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.batch-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.batch-header h3 {
  margin: 0;
}

.batch-details {
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
}

.detail-row .label {
  font-weight: 500;
  color: #7f8c8d;
}

.batch-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #ecf0f1;
  border-radius: 4px;
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

.batch-actions {
  display: flex;
  gap: 0.5rem;
}

.batch-actions .btn {
  flex: 1;
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
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
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
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
</style>
