# 🧠 AI Medical Healthcare Assistant

An intelligent healthcare chatbot powered by Groq LLM, LangChain, and FAISS vector search that provides preliminary medical guidance based on symptoms. Features emergency detection, risk assessment, and RAG (Retrieval-Augmented Generation) for accurate medical information.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.9-green)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ⚠️ Medical Disclaimer

**This system provides general medical information only and does NOT replace professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with any questions you may have regarding a medical condition.**

---

## 🎯 Features

- **🚨 Emergency Detection**: Multi-layered emergency detection using rule-based and AI-powered classifiers
- **👶 Pediatric Mode**: Specialized emergency protocols for infant patients
- **📊 Risk Assessment**: Automated symptom analysis and risk level scoring
- **🔍 RAG-Powered Responses**: Context-aware medical guidance using vector search over medical knowledge base
- **📝 Doctor Reports**: Generate downloadable medical summary reports
- **💾 Patient Records**: Secure SQLite database for tracking consultation history
- **🛡️ Input Validation**: Comprehensive security measures and error handling
- **📊 Conversation History**: Track and review previous consultations

---

## 📸 Screenshots

### Streamlit User Interface
![Screenshot 2026-02-03 004057](https://github.com/user-attachments/assets/890af2b7-da96-4fe2-b88e-2c9b9b32d564)
*Main interface with symptom input, patient profile selection, and risk assessment display*

### Code Architecture
![Screenshot 2026-02-02 230314](https://github.com/user-attachments/assets/fd7eea3e-f8e5-4dfe-adbb-e0911c213ad2)

*Modular architecture with separation of concerns*

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                      │
│                        (app.py)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Medical Agent Core                        │
│                   (main_agent.py)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Emergency   │  │   Symptom    │  │  Risk        │    │
│  │  Detection   │  │   Analyzer   │  │  Assessment  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌─────▼─────┐  ┌──────▼──────┐
│   Groq LLM   │  │  RAG      │  │  Database   │
│   (Llama)    │  │  Engine   │  │  (SQLite)   │
└──────────────┘  └───────────┘  └─────────────┘
                       │
                ┌──────▼──────┐
                │    FAISS    │
                │   Vector    │
                │    Store    │
                └─────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **LLM** | Groq (Llama 3.3 70B) |
| **Framework** | LangChain |
| **Vector Store** | FAISS |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **Database** | SQLite |
| **PDF Processing** | PyPDF |
| **Language** | Python 3.8+ |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Conda (recommended) or virtualenv
- Groq API key ([Get it here](https://console.groq.com/keys))

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ai-medical-healthcare.git
cd ai-medical-healthcare
```

### Step 2: Create Virtual Environment
```bash
# Using conda (recommended)
conda create -n medical_ai python=3.8
conda activate medical_ai

# Or using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
```

### Step 5: Prepare Medical Knowledge Base
Place your medical PDF documents in the project root as `knowledge_base.pdf` or in a `knowledge_base/` directory.

### Step 6: Build Vector Store
```bash
python ingest_pdfs.py
```

This will:
- Load and chunk your medical PDFs
- Generate embeddings using Sentence Transformers
- Create a FAISS vector index
- Save to `vector_store/medical/`

### Step 7: Run the Application
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

---

## 📁 Project Structure

```
ai-medical-healthcare/
├── app.py                      # Streamlit frontend
├── main_agent.py               # Core orchestration logic
├── Config.py                   # Configuration settings
├── ingest_pdfs.py             # Vector store creation script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                 # Git ignore rules
│
├── ai_core/                    # Core AI modules
│   ├── __init__.py
│   ├── llm_client.py          # Groq LLM wrapper
│   ├── rag_engine.py          # RAG implementation
│   ├── safety_guard.py        # Emergency detection
│   ├── emergency_handler.py   # Emergency response
│   ├── symptom_analyzer.py    # Symptom parsing
│   ├── disease_risk_engine.py # Risk assessment
│   ├── medicine_guard.py      # Medicine suggestions
│   └── report_analyzer.py     # Medical report analysis
│
├── utils/                      # Utility functions
│   ├── helpers.py             # Database operations
│   ├── pdf_loader.py          # PDF processing
│   ├── rag_engine.py          # Vector search
│   └── report_generator.py    # Report generation
│
├── database/                   # SQLite database
│   └── patient_records.db
│
├── vector_store/              # FAISS indices
│   └── medical/
│
├── logs/                       # Application logs
│   └── medical_app.log
│
└── screenshots/               # UI screenshots
    ├── streamlit_ui.png
    └── code_structure.png
```

---

## 🚀 Usage

### Basic Workflow

1. **Select Patient Profile**: Choose between "Adult" or "Infant" mode
2. **Enter Symptoms**: Describe symptoms in natural language
3. **Click Analyze**: System processes through multiple safety layers
4. **View Results**:
   - Risk assessment score
   - Medical guidance
   - Downloadable doctor report
5. **Review History**: Access previous consultations in sidebar

### Emergency Detection

The system uses three-layer emergency detection:

1. **Rule-Based**: Keyword matching for critical symptoms
   - Chest pain, difficulty breathing, unconsciousness, etc.
   
2. **AI-Powered**: LLM classification for context-aware detection
   
3. **Infant-Specific**: Specialized rules for pediatric emergencies
   - Not feeding, lethargy, blue lips, etc.

If an emergency is detected, the system immediately displays:
> 🚨 **This may be an emergency.**  
> Please seek immediate medical attention or contact emergency services immediately.

---

## 🔒 Security Features

- ✅ **Input Validation**: Length limits, type checking, sanitization
- ✅ **Error Handling**: Comprehensive try-catch blocks throughout
- ✅ **Logging**: Audit trail of all operations
- ✅ **Environment Variables**: API keys never hardcoded
- ✅ **Safe Deserialization**: Protected vector store loading
- ✅ **SQL Injection Protection**: Parameterized queries
- ✅ **.gitignore**: Sensitive files excluded from repository

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API authentication key | *Required* |
| `MODEL_NAME` | LLM model to use | `llama-3.3-70b-versatile` |

### Adjustable Parameters

In `ai_core/llm_client.py`:
```python
temperature=0.2        # LLM creativity (0.0-1.0)
```

In `utils/rag_engine.py`:
```python
k=3                    # Number of documents to retrieve
chunk_size=800         # PDF chunk size
chunk_overlap=150      # Chunk overlap for context
```

---

## 🧪 Testing

```bash
# Test vector store creation
python ingest_pdfs.py

# Test emergency detection
python -c "from ai_core.safety_guard import rule_based_emergency; print(rule_based_emergency('chest pain'))"

# Run application
streamlit run app.py
```

---

## 📊 Sample Queries

```
✅ "I have a fever of 101°F, cough, and body aches for 2 days"
✅ "Severe headache with nausea and sensitivity to light"
✅ "My baby is not feeding well and seems lethargic"
✅ "Persistent pain in lower right abdomen"

🚨 Emergency triggers:
- "Severe chest pain radiating to left arm"
- "Difficulty breathing and blue lips"
- "Sudden loss of consciousness"
```

---

## 🐛 Troubleshooting

### Issue: "Vector store not found"
**Solution**: Run `python ingest_pdfs.py` to create the FAISS index

### Issue: "GROQ_API_KEY not found"
**Solution**: Create `.env` file with your API key

### Issue: "Module not found" errors
**Solution**: Ensure virtual environment is activated and run:
```bash
pip install -r requirements.txt
```

### Issue: LLM model decommissioned
**Solution**: Update model name in `ai_core/llm_client.py` to a current model

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include error handling
- Update README for new features
- Test thoroughly before submitting

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Known Limitations

- Risk assessment uses basic keyword matching (not ML-based)
- Emergency detection may have false positives/negatives
- Not validated by medical professionals
- No real-time monitoring or follow-up
- Limited to text-based consultations
- Requires internet connection for LLM API

---

## 🔮 Future Enhancements

- [ ] ML-based symptom analysis and risk prediction
- [ ] Multi-language support
- [ ] Voice input/output capabilities
- [ ] Integration with telemedicine platforms
- [ ] Real-time vital signs monitoring
- [ ] Personalized health tracking
- [ ] Medication interaction checking
- [ ] Lab report analysis with computer vision
- [ ] FHIR standard compliance
- [ ] Mobile application

---

## 👥 Authors

- **Ruhul Amin Maruf** - *Initial work* - [GitHub](https://github.com/marufhasan-122)

---

## 🙏 Acknowledgments

- **Groq** for providing fast LLM inference
- **LangChain** for the RAG framework
- **Streamlit** for the elegant UI framework
- Medical knowledge base contributors
- Open-source community

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/marufhasan-122/ai-medical-healthcare/issues)
- Email: ruhulamin43416@gmail.com

---

## 📈 Project Status

**Status**: Active Development 🚧

**Version**: 1.0.0

**Last Updated**: February 2026

---

<div align="center">

**⚕️ Built with care for better healthcare accessibility ⚕️**

[Report Bug](https://github.com/yourusername/ai-medical-healthcare/issues) · [Request Feature](https://github.com/yourusername/ai-medical-healthcare/issues)

</div>
