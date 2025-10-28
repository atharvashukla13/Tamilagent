# -*- coding: utf-8 -*-
"""
Flask API for Tamil Agricultural Page Prediction Model
"""

from flask import Flask, request, jsonify, render_template
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from collections import Counter
import pandas as pd

app = Flask(__name__)

class TamilPagePredictor:
    def __init__(self, knowledge_base_path="TamilKnowledgeBase.json"):
        """Initialize the Tamil page prediction model"""
        self.model = SentenceTransformer("l3cube-pune/indic-sentence-similarity-sbert")
        self.knowledge_base = self.load_knowledge_base(knowledge_base_path)
        self.candidates = []
        self.candidate_texts = []
        self.candidate_embeddings = None
        self.prepare_candidates()
        
    def load_knowledge_base(self, path):
        """Load Tamil knowledge base from JSON file"""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def prepare_candidates(self):
        """Prepare candidate embeddings for similarity matching"""
        for feature in self.knowledge_base['features']:
            page_name = feature['page_name']
            for keyword in feature['keywords']:
                self.candidates.append(page_name)
                self.candidate_texts.append(keyword)
        
        # Encode all candidate texts
        self.candidate_embeddings = self.model.encode(self.candidate_texts)
        print(f"✅ Loaded {len(self.candidates)} Tamil candidates")
    
    def predict_page(self, query_text):
        """Predict the most relevant page for Tamil query"""
        # Encode the query
        query_embedding = self.model.encode([query_text])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.candidate_embeddings)
        
        # Get top predictions
        top_indices = np.argsort(similarities[0])[::-1][:5]  # Top 5
        
        results = []
        for idx in top_indices:
            results.append({
                'page_name': self.candidates[idx],
                'keyword': self.candidate_texts[idx],
                'similarity_score': float(similarities[0][idx]),
                'description': self.get_page_description(self.candidates[idx])
            })
        
        return results
    
    def get_page_description(self, page_name):
        """Get description for a page"""
        for feature in self.knowledge_base['features']:
            if feature['page_name'] == page_name:
                return feature.get('description', '')
        return ''

# Initialize the predictor
predictor = TamilPagePredictor()

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

@app.route('/visualize/keywords', methods=['GET'])
def visualize_keywords():
    """Create visualization of keyword distribution"""
    try:
        # Prepare data for visualization
        page_names = []
        keyword_counts = []
        
        for feature in predictor.knowledge_base['features']:
            page_names.append(feature['page_name'].replace('_', ' ').title())
            keyword_counts.append(len(feature['keywords']))
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        bars = plt.bar(range(len(page_names)), keyword_counts, color='skyblue', alpha=0.7)
        plt.xlabel('Pages')
        plt.ylabel('Number of Keywords')
        plt.title('Keyword Distribution Across Tamil Agricultural Pages')
        plt.xticks(range(len(page_names)), page_names, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, count in zip(bars, keyword_counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'image': f"data:image/png;base64,{img_str}",
            'data': {
                'page_names': page_names,
                'keyword_counts': keyword_counts
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/visualize/similarity', methods=['POST'])
def visualize_similarity():
    """Create similarity heatmap for a query"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query text is required'}), 400
        
        query_text = data['query']
        predictions = predictor.predict_page(query_text)
        
        # Prepare data for heatmap
        page_names = [pred['page_name'].replace('_', ' ').title() for pred in predictions[:10]]
        similarity_scores = [pred['similarity_score'] for pred in predictions[:10]]
        
        # Create heatmap
        plt.figure(figsize=(10, 6))
        colors = plt.cm.RdYlBu_r(np.array(similarity_scores))
        bars = plt.barh(range(len(page_names)), similarity_scores, color=colors)
        
        plt.xlabel('Similarity Score')
        plt.ylabel('Pages')
        plt.title(f'Similarity Scores for Query: "{query_text}"')
        plt.yticks(range(len(page_names)), page_names)
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars, similarity_scores)):
            plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{score:.3f}', ha='left', va='center')
        
        plt.tight_layout()
        
        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'image': f"data:image/png;base64,{img_str}",
            'query': query_text,
            'predictions': predictions[:10]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    app.run(debug=True, host='0.0.0.0', port=5000)
