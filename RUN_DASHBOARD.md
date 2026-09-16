# Run the Website

Open a terminal in the project root.

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Build/rebuild the warehouse

```bash
python -m etl.pipeline
```

## 3. Start the website

```bash
streamlit run dashboard.py
```

The dashboard will normally open at:

`http://localhost:8501`

If the browser does not open automatically, copy the Local URL printed in the terminal into your browser.
