## Project Structure

meeting_translator_app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── real_time_main.py
│   │   ├── services/
│   │   │   ├── transcription_service.py
│   │   │   └── translation_service.py
│   │   └── utils/
│   │       └── tocken_generator.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│       ├── test_transcription.py
│       └── test_translation.py
├── frontend/
│   ├── public/
│   ├── public/
│   │   ├── index.html
│   │   ├── script.js
│   │   ├── styles.css
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md
└── .github/
    └── workflows/
        └── ci_cd_pipeline.yml
