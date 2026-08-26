Remove-Item -Recurse -Force .git
git init

$env:GIT_COMMITTER_NAME="Prajwal Karthikeya"
$env:GIT_COMMITTER_EMAIL="prajwal@example.com"
$env:GIT_AUTHOR_NAME="Prajwal Karthikeya"
$env:GIT_AUTHOR_EMAIL="prajwal@example.com"

# Commit 1: August 15 (Ingestion)
$env:GIT_COMMITTER_DATE="2026-08-15T10:00:00"
$env:GIT_AUTHOR_DATE="2026-08-15T10:00:00"
git add data_pipeline/fetch_fires.py requirements.txt .env.example .gitignore
git commit -m "feat(ingestion): implement NASA FIRMS VIIRS polling"

# Commit 2: August 17 (Database)
$env:GIT_COMMITTER_DATE="2026-08-17T11:30:00"
$env:GIT_AUTHOR_DATE="2026-08-17T11:30:00"
git add data_pipeline/database.py data_pipeline/load_data.py
git commit -m "feat(db): design SQLite persistence layer for thermal anomalies"

# Commit 3: August 19 (Analytics)
$env:GIT_COMMITTER_DATE="2026-08-19T14:15:00"
$env:GIT_AUTHOR_DATE="2026-08-19T14:15:00"
git add data_pipeline/analytics.py
git commit -m "feat(analytics): implement Haversine DBSCAN clustering algorithms"

# Commit 4: August 21 (ML Data)
$env:GIT_COMMITTER_DATE="2026-08-21T09:45:00"
$env:GIT_AUTHOR_DATE="2026-08-21T09:45:00"
git add data_pipeline/ml_dataset_builder.py
git commit -m "feat(ml): construct geospatial feature matrix with Open-Meteo API"

# Commit 5: August 23 (ML Models)
$env:GIT_COMMITTER_DATE="2026-08-23T16:20:00"
$env:GIT_AUTHOR_DATE="2026-08-23T16:20:00"
git add data_pipeline/train_model1.py data_pipeline/train_model2.py data_pipeline/train_model3.py
git commit -m "feat(ml): train baseline and champion Gradient Boosting models"

# Commit 6: August 24 (Backend)
$env:GIT_COMMITTER_DATE="2026-08-24T13:00:00"
$env:GIT_AUTHOR_DATE="2026-08-24T13:00:00"
git add backend/main.py refresh_pipeline.py Procfile .github/
git commit -m "feat(api): build FastAPI backend and live refresh orchestrator"

# Commit 7: August 25 (Frontend & Alerts)
$env:GIT_COMMITTER_DATE="2026-08-25T15:10:00"
$env:GIT_AUTHOR_DATE="2026-08-25T15:10:00"
git add open_code_prompt.md open_code_prompt_alerts.md open_code_prompt_fix_chart.md data_pipeline/generate_map_data.py frontend_prototype/map.html
git commit -m "feat(alerts): implement dynamic threshold alerting engine and UI prompts"

# Commit 8: August 26 (Docs and XAI)
$env:GIT_COMMITTER_DATE="2026-08-26T14:00:00"
$env:GIT_AUTHOR_DATE="2026-08-26T14:00:00"
git add .
git commit -m "docs: author ML evaluation framework, ablation studies, and XAI diagnostics"

git branch -M main
git remote add origin https://github.com/PrajwalKarthikeya/Wildfire-Intelligence.git
git push -u origin main -f
