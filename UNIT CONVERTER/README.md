# Advanced Unit Converter

A Streamlit application for converting various units of measurement with interactive charts and history tracking.

## Deployment Instructions

### Deploying to Streamlit Cloud

1. Create a GitHub account if you don't have one
2. Create a new repository on GitHub
3. Push your code to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```
4. Go to [Streamlit Cloud](https://streamlit.io/cloud)
5. Sign in with your GitHub account
6. Click "New app"
7. Select your repository, branch, and main file (app.py)
8. Click "Deploy"

### Local Development

To run the app locally:

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   streamlit run app.py
   ```

## Features

- Multiple unit conversion categories
- Interactive conversion charts
- Conversion history tracking
- Adjustable precision
- Modern UI with responsive design 