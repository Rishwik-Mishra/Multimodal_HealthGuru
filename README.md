# 🚀 HealthGuru AI  
### Multimodal Nutrition Intelligence Backend

HealthGuru AI is a production-oriented multimodal AI system that integrates computer vision, structured nutrition databases, and portion-aware macro computation into a scalable backend architecture.

This is not just an ML model.  
It is a structured AI backend system designed with product-level architecture.

---

# 🎯 Vision

Build a Multimodal AI Health System that:

- Recognizes food from images using CNN
- Maps predictions to structured nutrition data
- Supports dish-level and ingredient-level resolution
- Handles portion-aware macro scaling
- Enables daily nutrition logging (next phase)
- Evolves into a Retrieval-Augmented (RAG) health decision-support system

---

# 🧠 System Architecture Overview

HealthGuru follows a layered AI backend architecture:

```
Image → CNN → Food Label
      → Mapping Layer → Dish / Ingredient
      → Portion Engine → Gram Resolution
      → Nutrition Engine → Macro Scaling
      → API Response (JSON)
```

---

# 🏗 High-Level Architecture

## 1️⃣ Vision Layer (Perception Engine)

- EfficientNetB0 CNN
- 121 food classes (Food41 + Fruits360 merged)
- 224×224 input
- Proper preprocessing pipeline
- ~78% Top-1 accuracy
- ~89% Top-3 accuracy

Pipeline:

```
Image → CNN → Label + Confidence
```

---

## 2️⃣ Nutrition Intelligence Layer

### Foundation Foods (USDA-Based)

- 365 scientifically verified foods
- Standardized per-100g storage
- Macronutrients:
  - Calories
  - Protein
  - Carbohydrates
  - Fat
  - Fiber
  - Sugar
  - Sodium
  - Saturated fat

All values stored per 100g for consistent scaling.

Clean canonical naming + ingestion pipeline included.

---

## 3️⃣ Dish Layer

- 121 dishes auto-seeded from CNN classes
- Curated macros for common dishes
- Fallback to ingredient mapping
- Clean separation from foundation foods

Pipeline:

```
CNN label → Dish table → (fallback) Foundation foods
```

---

## 4️⃣ Portion Intelligence Engine

Supports:

- Direct gram input
- Portion-based scaling:
  - piece
  - slice
  - bowl
  - cup
  - etc.

Dynamic gram resolution:

```
portion × portion_count → grams → macro scaling
```

Case-insensitive matching and flexible database resolution.

---

## 5️⃣ Macro Computation Engine

All nutrition stored per-100g.

Scaling formula:

```
scaled_value = (per_100g_value × grams) / 100
```

Ensures:
- Scientific consistency
- Easy extensibility
- Ingredient-composition compatibility (next phase)

---

## 6️⃣ API Layer (FastAPI)

Core endpoint:

```
POST /predict
```

Supports:

- Image upload
- grams (optional)
- portion (optional)
- portion_count (optional)

Returns:

- Detected food
- Confidence score
- Final grams used
- Scaled macros (JSON)

---

# 🗂 Current Project Structure

```
HEALTH_GURU/
│
├── app/
│   └── main.py
│
├── database/
│   ├── config.py
│   ├── init_db.py
│   ├── models.py
│   ├── session.py
│   ├── curated_dish_data.py
│   ├── seed.py
│   ├── seed_dishes.py
│   ├── seed_dish_portions.py
│   ├── usda_cleaner.py
│   └── usda_ingest.py
│
├── models/
│   └── cnn/
│       ├── healthguru_cnn_v1.keras
│       └── class_names.json
│
├── services/
│   ├── image_service.py
│   ├── mapping_service.py
│   ├── portion_service.py
│   ├── calorie_service.py
│   └── nlp_service.py
│
├── requirements.txt
└── README.md
```

---

# 🛠 Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- TensorFlow / Keras (CNN)
- NumPy
- Uvicorn

---

# 📊 Current System Capabilities

✔ Real-time image recognition  
✔ Structured nutrition database integration  
✔ Dish + ingredient resolution  
✔ Portion-aware macro scaling  
✔ Clean service-layer architecture  
✔ Production-ready backend structure  

---

# 🚧 Upcoming Features

## Phase 1 – Daily Logging System
- User table
- Food log table
- Macro snapshot storage
- Daily aggregation endpoint

## Phase 2 – Ingredient Composition Engine
- Dish → ingredient proportions
- Dynamic macro calculation
- Scientific transparency

## Phase 3 – Health Intelligence Layer
- Goal tracking
- Health scoring engine
- Calorie target recommendation

## Phase 4 – RAG Decision Support System
- Medical document ingestion
- Chunking strategies
- Embeddings
- Vector database integration
- Semantic search
- Context retrieval
- Citation-based health responses

---

# 💎 Resume Positioning

Designed and implemented a multimodal AI nutrition backend integrating CNN-based food recognition, structured USDA nutrition datasets, dynamic portion-aware macro computation, and scalable FastAPI architecture with PostgreSQL.

---

# 🚀 Running the Project

Start the server:

```bash
uvicorn app.main:app --reload
```

Open API documentation:

```
http://127.0.0.1:8000/docs
```

---

# 📌 Development Workflow

- Active development on `dev` branch
- Stable releases merged into `main`
- Modular service-layer architecture maintained
- Clean database-first design philosophy

---

HealthGuru AI is being developed as a scalable AI backend system with long-term extensibility toward a full AI-powered health decision-support platform.
