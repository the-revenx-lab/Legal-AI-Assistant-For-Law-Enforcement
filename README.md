# 🚓 Legal AI Assistant for Law Enforcement

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Rasa](https://img.shields.io/badge/Rasa-3.x-blueviolet)](https://rasa.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-orange)](https://www.mysql.com/)

---

## 📖 Description

**Legal AI Assistant for Law Enforcement** is a modern, AI-powered platform designed to assist law enforcement agencies with legal queries, FIR (First Information Report) management, and Indian Penal Code (IPC) section lookup. It combines a conversational AI chatbot (Rasa), a robust backend API (FastAPI), and a user-friendly web interface to streamline legal workflows and improve access to legal information.

---

## ✨ Features

- 🤖 Conversational AI chatbot for legal queries (IPC, crimes, punishments)
- 📝 FIR creation, management, and PDF export
- 📚 IPC section search and management
- 👮 User authentication and role-based access
- 📊 Admin dashboards for FIR and IPC data
- 🌐 Modern web interface (HTML/CSS/JS)
- 🗄️ MySQL database for persistent storage
- 🐳 Dockerized deployment and cloud-ready setup

---

## 📁 Folder Structure

```plaintext
chat/
├── actions/                # Custom Rasa actions
│   ├── __init__.py
│   └── actions.py
├── data/                   # Rasa NLU, rules, and stories
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
├── docs/                   # Documentation (API, deployment, schema, user guide)
│   ├── api.md
│   ├── deployment.md
│   ├── development.md
│   ├── schema.md
│   └── user_guide.md
├── models/                 # (Trained Rasa/ML models)
├── rasa/                   # Rasa project (actions, config, data)
├── rasa_data/              # Alternative/legacy Rasa data
├── static/                 # Web UI assets (HTML, CSS, JS, images)
├── tests/                  # Test files and test data
├── *.py                    # Backend scripts (API, DB, data processing)
├── *.sql                   # Database schema and migration files
├── *.yml                   # Configurations (Rasa, endpoints, etc.)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build instructions
├── docker-compose.yml      # Docker Compose setup
└── README.md               # Project documentation (this file)
```

---

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://pydantic-docs.helpmanual.io/)
- **Chatbot**: [Rasa](https://rasa.com/)
- **Database**: [MySQL](https://www.mysql.com/)
- **Frontend**: HTML, CSS, JavaScript
- **PDF Generation**: [ReportLab](https://www.reportlab.com/)
- **Containerization**: [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/)
- **Deployment**: Nginx, systemd, cloud platforms (Render, Railway, Vercel, Heroku)

---

## ⚡ Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/the-revenx-lab/Legal-AI-Assistant-For-Law-Enforcement.git
   cd Legal-AI-Assistant-For-Law-Enforcement
   ```

2. **Set up Python environment**
   ```sh
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env` and update with your settings, or edit `config.yml`/`credentials.yml`.

4. **Set up the database**
   ```sh
   # Start MySQL and create the database
   mysql -u root -p < schema.sql
   # Populate initial data
   python populate_database.py
   ```

5. **Train the Rasa model**
   ```sh
   rasa train
   ```

---

## ▶️ How to Run the Project

**Start the backend API:**
```sh
uvicorn fir_api:router --reload
```

**Start the Rasa action server:**
```sh
rasa run actions
```

**Start the Rasa server:**
```sh
rasa run --enable-api --cors "*"
```

**(Optional) Run with Docker Compose:**
```sh
docker-compose up --build
```

**Access the web UI:**
- Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🤝 Contribution Guidelines

1. Fork the repository and create your feature branch:
   ```sh
   git checkout -b feature/your-feature
   ```
2. Commit your changes with clear messages:
   ```sh
   git commit -m "feat: add new feature"
   ```
3. Push to your fork and submit a Pull Request.
4. Ensure your code follows the [development guide](docs/development.md) and passes all tests.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- Indian Penal Code (IPC) data and legal resources
- [Rasa Open Source](https://rasa.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- All contributors and law enforcement professionals

---

> _Empowering law enforcement with AI-driven legal assistance!_ 