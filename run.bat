@echo off
echo Installing required packages for the current Python environment...
python -m pip install streamlit pandas scikit-learn textblob requests --quiet
echo Downloading NLP models...
python -m textblob.download_corpora --quiet
echo Starting Streamlit App!
python -m streamlit run app.py
pause
