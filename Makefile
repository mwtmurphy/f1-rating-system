app:
	streamlit run src/f1_elo/app.py

env:
	poetry install

major:
	poetry version patch

minor:
	poetry version minor

patch:
	poetry version major
