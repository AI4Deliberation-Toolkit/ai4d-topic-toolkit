# ai4d-topic-toolkit

A Django app for multilingual topic extraction over civic-deliberation articles, with article-to-article similarity search. Uses sentence-transformers (mpnet) against a curated taxonomy of 18 parents and 91 leaves, labelled in English, Greek, and German.

## Quick start (Docker)

```
docker compose up
```

The app listens on port 8000. Endpoints (all under `/api/`):

- `POST /topics/extract-conversation` — extract topics for an article + its comments
- `GET  /topics/article/<id>` — latest stored extraction for an article
- `GET  /topics` — active taxonomy listing
- `GET  /articles/<platform>/<id>/similar` — article-to-article similarity

First boot downloads the embedding model (~1 GB) into a named volume; subsequent boots reuse it.

## Local development

```
python3.12 -m venv .venv
source .venv/bin/activate
pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
python manage.py migrate
python manage.py seed_taxonomy
python manage.py test
```

## License

EUPL v1.2 — see [LICENSE](LICENSE).
