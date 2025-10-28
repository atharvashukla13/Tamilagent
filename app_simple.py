# -*- coding: utf-8 -*-
"""
Simplified Flask API for Tamil Agricultural Page Prediction Model
This version uses simple keyword matching instead of sentence transformers for demo purposes
"""

from flask import Flask, request, jsonify, render_template
import json
import numpy as np
from collections import Counter
import pandas as pd

app = Flask(__name__)

class SimpleTamilPagePredictor:
    def __init__(self, knowledge_base_path="TamilKnowledgeBase.json"):
        """Initialize the Tamil page prediction model with simple keyword matching"""
        self.knowledge_base = self.load_knowledge_base(knowledge_base_path)
        self.prepare_keyword_index()
        
    def load_knowledge_base(self, path):
        """Load Tamil knowledge base from JSON file"""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def prepare_keyword_index(self):
        """Prepare keyword index for simple matching"""
        self.keyword_to_page = {}
        self.page_keywords = {}
        
        for feature in self.knowledge_base['features']:
            page_name = feature['page_name']
            keywords = feature['keywords']
            self.page_keywords[page_name] = keywords
            
            for keyword in keywords:
                if keyword not in self.keyword_to_page:
                    self.keyword_to_page[keyword] = []
                self.keyword_to_page[keyword].append(page_name)
        
        print(f"Loaded {len(self.keyword_to_page)} Tamil keywords for {len(self.page_keywords)} pages")
    
    def predict_page(self, query_text):
        """Predict the most relevant page for Tamil query using simple keyword matching"""
        query_words = query_text.lower().split()
        
        # Calculate scores for each page
        page_scores = {}
        
        for word in query_words:
            for keyword, pages in self.keyword_to_page.items():
                if word in keyword.lower() or keyword.lower() in word:
                    for page in pages:
                        if page not in page_scores:
                            page_scores[page] = 0
                        page_scores[page] += 1
        
        # If no matches found, return all pages with zero scores
        if not page_scores:
            page_scores = {page: 0 for page in self.page_keywords.keys()}
        
        # Sort by score
        sorted_pages = sorted(page_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for page_name, score in sorted_pages[:5]:  # Top 5
            # Find matching keyword
            matching_keyword = ""
            for keyword in self.page_keywords[page_name]:
                if any(word in keyword.lower() for word in query_words):
                    matching_keyword = keyword
                    break
            
            if not matching_keyword and self.page_keywords[page_name]:
                matching_keyword = self.page_keywords[page_name][0]
            
            results.append({
                'page_name': page_name,
                'keyword': matching_keyword,
                'similarity_score': score / max(len(query_words), 1),  # Normalize by query length
                'description': self.get_page_description(page_name)
            })
        
        return results
    
    def get_page_description(self, page_name):
        """Get description for a page"""
        for feature in self.knowledge_base['features']:
            if feature['page_name'] == page_name:
                return feature.get('description', '')
        return ''

# Initialize the predictor
predictor = SimpleTamilPagePredictor()

@app.route('/')
def home():
    """Home page with API documentation"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query text is required'}), 400
        
        query_text = data['query']
        if not query_text.strip():
            return jsonify({'error': 'Query text cannot be empty'}), 400
        
        # Get predictions
        predictions = predictor.predict_page(query_text)
        
        return jsonify({
            'query': query_text,
            'predictions': predictions,
            'top_prediction': predictions[0] if predictions else None
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['GET'])
def predict_get():
    """GET endpoint for prediction with query parameter"""
    query_text = request.args.get('query', '')
    if not query_text:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        predictions = predictor.predict_page(query_text)
        return jsonify({
            'query': query_text,
            'predictions': predictions,
            'top_prediction': predictions[0] if predictions else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pages', methods=['GET'])
def get_pages():
    """Get all available pages and their keywords"""
    pages = []
    for feature in predictor.knowledge_base['features']:
        pages.append({
            'page_name': feature['page_name'],
            'keywords': feature['keywords'],
            'description': feature.get('description', ''),
            'action_message': feature.get('action_message', '')
        })
    
    return jsonify({'pages': pages})

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about the knowledge base"""
    total_pages = len(predictor.knowledge_base['features'])
    total_keywords = sum(len(feature['keywords']) for feature in predictor.knowledge_base['features'])
    
    # Count keywords per page
    keyword_counts = [len(feature['keywords']) for feature in predictor.knowledge_base['features']]
    
    stats = {
        'total_pages': total_pages,
        'total_keywords': total_keywords,
        'avg_keywords_per_page': total_keywords / total_pages if total_pages > 0 else 0,
        'keyword_distribution': {
            'min': min(keyword_counts) if keyword_counts else 0,
            'max': max(keyword_counts) if keyword_counts else 0,
            'median': np.median(keyword_counts) if keyword_counts else 0
        }
    }
    
    return jsonify(stats)

@app.route('/test', methods=['GET'])
def test_endpoints():
    """Test endpoint with sample Tamil queries"""
    sample_queries = [
        "என்டிவிஐ மூலம் பயிர்களின் ஆரோக்கியத்தை மதிப்பிடலாம்",
        "விளைச்சல் முன்னறிவிப்பு",
        "பயிர்நோய் கண்டறிதல்",
        "நீர்ப்பாசனத் திட்டம்",
        "பயிர் பரிந்துரை"
    ]
    
    results = []
    for query in sample_queries:
        predictions = predictor.predict_page(query)
        results.append({
            'query': query,
            'top_prediction': predictions[0] if predictions else None
        })
    
    return jsonify({'test_results': results})

if __name__ == '__main__':
    print("Starting Tamil Agricultural Page Prediction API...")
    print("This is a simplified version using keyword matching")
    print("For full sentence transformer functionality, install: pip install sentence-transformers")
    app.run(debug=True, host='0.0.0.0', port=5000)
