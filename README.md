# OVERLOAD VEHICLE DETECTION

## Features
- Vehicle overload detection using Roboflow API
- User authentication system (login/register)
- Bounding box visualization
- Dynamic background images

## Quick Start
1. Clone the repository:
```bash
git clone https://github.com/Tharun-coder-hash/Overload.git
cd Overload
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python -m streamlit run app.py
```

## Important Note
Update deprecated Streamlit code in `app.py` and `auth.py`:
```python
# Replace:
query_params = st.experimental_get_query_params()

# With:
query_params = st.query_params()
```

## Project Structure

- **Overload/**
  - `app.py` - Main Streamlit application
  - `auth.py` - User authentication handlers
  - `login.py` - Login page logic
  - `requirements.txt` - Python dependencies
```

## License
MIT License
