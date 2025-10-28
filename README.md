# Tamil Agricultural Page Prediction API 🌾

A Flask-based API that uses Tamil language processing to predict the most relevant agricultural pages based on user queries. The system leverages sentence transformers and cosine similarity to match Tamil queries with appropriate agricultural features.

## Features ✨

- **Tamil Language Support**: Processes Tamil agricultural queries using Indic sentence transformers
- **Page Prediction**: Predicts the most relevant agricultural page based on Tamil input
- **Visualization**: Interactive charts and heatmaps for model insights
- **Web Interface**: User-friendly web interface for testing the API
- **Multiple Endpoints**: Comprehensive API with various endpoints for different functionalities

## Installation 🚀

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd AgriFormerTamil
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (if needed):
   ```python
   import nltk
   nltk.download('punkt')
   ```

## Usage 📖

### Starting the API Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Web Interface

Open your browser and navigate to `http://localhost:5000` to access the interactive web interface.

## API Endpoints 📡

### 1. Main Prediction Endpoint

**POST** `/predict`

Predicts the most relevant page for a Tamil query.

**Request Body**:

```json
{
  "query": "என்டிவிஐ மூலம் பயிர்களின் ஆரோக்கியத்தை மதிப்பிடலாம்"
}
```

**Response**:

```json
{
  "query": "என்டிவிஐ மூலம் பயிர்களின் ஆரோக்கியத்தை மதிப்பிடலாம்",
  "predictions": [
    {
      "page_name": "satellite_analysis",
      "keyword": "என்டிவிஐ",
      "similarity_score": 0.8234,
      "description": "செயற்கைக்கோள் பகுப்பாய்வு பக்கத்தை திறக்கலாம்"
    }
  ],
  "top_prediction": {
    "page_name": "satellite_analysis",
    "keyword": "என்டிவிஐ",
    "similarity_score": 0.8234,
    "description": "செயற்கைக்கோள் பகுப்பாய்வு பக்கத்தை திறக்கலாம்"
  }
}
```

### 2. GET Prediction Endpoint

**GET** `/predict?query=<tamil_text>`

Same functionality as POST endpoint but using GET method.

### 3. Get All Pages

**GET** `/pages`

Returns all available pages and their keywords.

### 4. Statistics

**GET** `/stats`

Returns statistics about the knowledge base.

### 5. Keyword Visualization

**GET** `/visualize/keywords`

Returns a bar chart showing keyword distribution across pages.

### 6. Similarity Visualization

**POST** `/visualize/similarity`

Creates a similarity heatmap for a given query.

**Request Body**:

```json
{
  "query": "விளைச்சல் முன்னறிவிப்பு"
}
```

### 7. Test Endpoint

**GET** `/test`

Tests the API with sample Tamil queries.

## Sample Tamil Queries 🗣️

| Tamil Query                                         | English Translation                   | Expected Page              |
| --------------------------------------------------- | ------------------------------------- | -------------------------- |
| என்டிவிஐ மூலம் பயிர்களின் ஆரோக்கியத்தை மதிப்பிடலாம் | Assess crop health through NDVI       | satellite_analysis         |
| விளைச்சல் முன்னறிவிப்பு                             | Yield prediction                      | yield_prediction           |
| பயிர்நோய் கண்டறிதல்                                 | Crop disease detection                | crop_disease               |
| நீர்ப்பாசனத் திட்டம்                                | Irrigation plan                       | irrigation_plan            |
| பயிர் பரிந்துரை                                     | Crop recommendation                   | crop_recommendation        |
| உரம் மற்றும் பூச்சிக்கொல்லி அறிவகம்                 | Fertilizer and pesticide encyclopedia | fertilizer_pesticide_pedia |

## Available Pages 📄

The system supports prediction for the following agricultural pages:

1. **yield_prediction** - விளைச்சல் முன்னறிவிப்பு
2. **satellite_analysis** - செயற்கைக்கோள் பகுப்பாய்வு
3. **crop_disease** - பயிர்நோய்
4. **irrigation_plan** - நீர்ப்பாசனத் திட்டம்
5. **crop_recommendation** - பயிர் பரிந்துரை
6. **fertilizer_pesticide_pedia** - உரம் மற்றும் பூச்சிக்கொல்லி அறிவகம்
7. **simulation_game** - பயிற்சி விளையாட்டு
8. **farming_guide** - விவசாய வழிகாட்டி
9. **fertilizer_check** - உரம் சரிபார்ப்பு
10. **community** - சமூகம்
11. **government_schemes** - அரசுத் திட்டங்கள்
12. **agri_expert_chatbot** - விவசாய நிபுணர் அரட்டை
13. **pest_detection** - பூச்சி கண்டறிதல்
14. **pest_report** - பூச்சி அறிக்கை
15. **pest_map** - பூச்சி வரைபடம்
16. **live_market_price** - நேரடி சந்தை விலை
17. **agriculture_news** - விவசாய செய்திகள்
18. **farms_and_tools** - வயல்கள் மற்றும் கருவிகள்
19. **farmer_to_farmer_trade** - விவசாயி-விவசாயி வர்த்தகம்
20. **farmer_dashboard** - விவசாயி டாஷ்போர்டு

## Technical Details 🔧

### Model Architecture

- **Sentence Transformer**: `l3cube-pune/indic-sentence-similarity-sbert`
- **Similarity Metric**: Cosine similarity
- **Language**: Tamil (Indic script)
- **Framework**: Flask with sentence-transformers

### Knowledge Base Structure

The knowledge base (`TamilKnowledgeBase.json`) contains:

- Page names (English identifiers)
- Tamil keywords for each page
- Tamil descriptions
- Action messages

### Performance

- **Response Time**: ~200-500ms per prediction
- **Accuracy**: High similarity scores for relevant Tamil queries
- **Scalability**: Can handle multiple concurrent requests

## Development 👨‍💻

### Project Structure

```
AgriFormerTamil/
├── app.py                          # Main Flask application
├── TamilAgriformer.py             # Original model code
├── TamilKnowledgeBase.json        # Tamil knowledge base
├── requirements.txt               # Python dependencies
├── templates/
│   └── index.html                 # Web interface
└── README.md                      # This file
```

### Adding New Pages

To add new pages to the system:

1. Edit `TamilKnowledgeBase.json`
2. Add new feature with Tamil keywords
3. Restart the Flask server

### Customizing the Model

You can modify the sentence transformer model by changing the model name in `app.py`:

```python
self.model = SentenceTransformer("your-model-name")
```

## API Testing 🧪

### Using cURL

```bash
# Test prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"query": "விளைச்சல் முன்னறிவிப்பு"}'

# Get statistics
curl http://localhost:5000/stats

# Get all pages
curl http://localhost:5000/pages
```

### Using Python

```python
import requests

# Test prediction
response = requests.post('http://localhost:5000/predict',
                        json={'query': 'விளைச்சல் முன்னறிவிப்பு'})
print(response.json())
```

## Troubleshooting 🔧

### Common Issues

1. **Model Loading Error**: Ensure all dependencies are installed correctly
2. **Tamil Text Not Displaying**: Check browser font support for Tamil
3. **Slow Response**: First request may be slower due to model loading

### Error Codes

- `400`: Bad Request (missing or invalid query)
- `500`: Internal Server Error (model or processing error)

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is open source and available under the MIT License.

## Acknowledgments 🙏

- Tamil language processing capabilities powered by Indic sentence transformers
- Agricultural domain knowledge from Tamil farming community
- Flask framework for API development
- Sentence-transformers library for semantic similarity

---

**Made with ❤️ for Tamil Agricultural Community**
