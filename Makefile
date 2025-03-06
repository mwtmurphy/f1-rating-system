INT_DIR = data/interim
RAW_DIR = data/raw
SRC_DIR = src/f1_rating_system

app:
	poetry run streamlit run ${SRC_DIR}/app.py

data_e2e:
	make data_preprocessed
	make data_features
	make data_model
	make data_report

data_features: ${INT_DIR}/preprocessed_data.csv
	poetry run python ${SRC_DIR}/features.py

data_model: ${INT_DIR}/features.csv
	poetry run python ${SRC_DIR}/model.py

data_preprocessed: ${RAW_DIR}/races.csv ${RAW_DIR}/results.csv
	poetry run python ${SRC_DIR}/data.py

data_report: ${INT_DIR}/modelled_data.csv
	poetry run python ${SRC_DIR}/report.py

env:
	poetry install

major:
	poetry version patch

minor:
	poetry version minor

patch:
	poetry version major
