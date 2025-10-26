#!/usr/bin/env python3
"""
Unit tests for the API server
"""
import unittest
import json
from unittest.mock import Mock, patch
from api_server import app


class TestAPIServer(unittest.TestCase):
    """Test cases for API server endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app.test_client()
        self.app.testing = True
        
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
    
    def test_get_config(self):
        """Test config endpoint"""
        response = self.app.get('/api/config')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('target_language', data)
        self.assertIn('use_azure', data)
        self.assertIn('model', data)
    
    def test_get_glossary(self):
        """Test glossary endpoint"""
        response = self.app.get('/api/glossary')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('terms', data)
        self.assertIsInstance(data['terms'], list)
    
    def test_list_batches_empty(self):
        """Test listing batches when none exist"""
        response = self.app.get('/api/batches')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('batches', data)
        self.assertIsInstance(data['batches'], list)


if __name__ == '__main__':
    unittest.main(verbosity=2)
