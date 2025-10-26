<template>
  <div class="glossary-manager">
    <div class="header">
      <h2>Translation Glossary</h2>
      <button @click="showAddModal = true" class="btn btn-primary">
        + Add Term
      </button>
    </div>

    <div v-if="loading" class="loading">Loading glossary...</div>
    
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="success" class="success">{{ success }}</div>

    <div class="card">
      <div class="glossary-info info">
        <strong>Translation Memory:</strong> Terms defined here will be used consistently 
        across all translations to ensure terminology accuracy.
      </div>

      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search terms..." 
          class="input"
        />
      </div>

      <div class="glossary-list">
        <div class="glossary-header">
          <div class="term-col">Source Term (English)</div>
          <div class="term-col">Target Translation</div>
        </div>
        
        <div 
          v-for="(term, index) in filteredTerms" 
          :key="index" 
          class="glossary-item"
        >
          <div class="term-col">{{ term.source }}</div>
          <div class="term-col">{{ term.target }}</div>
        </div>

        <div v-if="filteredTerms.length === 0" class="no-terms">
          No terms found. Add your first term to get started.
        </div>
      </div>
    </div>

    <!-- Add Term Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Add Glossary Term</h3>
          <button @click="showAddModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Source Term (English)</label>
            <input 
              v-model="newTerm.source" 
              class="input" 
              placeholder="e.g., Knowledge Base"
              @keyup.enter="addTerm"
            />
          </div>
          <div class="form-group">
            <label>Target Translation</label>
            <input 
              v-model="newTerm.target" 
              class="input" 
              placeholder="e.g., ナレッジベース"
              @keyup.enter="addTerm"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAddModal = false" class="btn btn-secondary">Cancel</button>
          <button 
            @click="addTerm" 
            class="btn btn-primary"
            :disabled="!newTerm.source || !newTerm.target || adding"
          >
            {{ adding ? 'Adding...' : 'Add Term' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'GlossaryManager',
  data() {
    return {
      terms: [],
      loading: false,
      error: null,
      success: null,
      searchQuery: '',
      showAddModal: false,
      newTerm: {
        source: '',
        target: ''
      },
      adding: false
    };
  },
  computed: {
    filteredTerms() {
      if (!this.searchQuery) return this.terms;
      
      const query = this.searchQuery.toLowerCase();
      return this.terms.filter(term => 
        term.source.toLowerCase().includes(query) ||
        term.target.toLowerCase().includes(query)
      );
    }
  },
  mounted() {
    this.loadGlossary();
  },
  methods: {
    async loadGlossary() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.getGlossary();
        this.terms = response.data.terms;
      } catch (err) {
        this.error = 'Failed to load glossary: ' + err.message;
      } finally {
        this.loading = false;
      }
    },
    async addTerm() {
      if (!this.newTerm.source || !this.newTerm.target) {
        return;
      }

      this.adding = true;
      this.error = null;
      this.success = null;
      try {
        await api.addGlossaryTerm(this.newTerm.source, this.newTerm.target);
        this.success = 'Term added successfully!';
        this.showAddModal = false;
        this.newTerm = { source: '', target: '' };
        await this.loadGlossary();
        
        // Clear success message after 3 seconds
        setTimeout(() => {
          this.success = null;
        }, 3000);
      } catch (err) {
        this.error = 'Failed to add term: ' + err.message;
      } finally {
        this.adding = false;
      }
    }
  }
};
</script>

<style scoped>
.glossary-manager {
  padding: 1rem 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.glossary-info {
  margin-bottom: 1.5rem;
}

.search-box {
  margin-bottom: 1.5rem;
}

.glossary-list {
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
}

.glossary-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  font-weight: 600;
  border-bottom: 2px solid #e9ecef;
}

.glossary-item {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.glossary-item:hover {
  background-color: #f8f9fa;
}

.glossary-item:last-child {
  border-bottom: none;
}

.term-col {
  padding: 0.25rem;
}

.no-terms {
  padding: 2rem;
  text-align: center;
  color: #7f8c8d;
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
