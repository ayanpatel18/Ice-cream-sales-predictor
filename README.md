# ScoopSignal

Ice cream sales predictor website trained from ice-cream.csv with a regression model and a 70/30 train-test split.

## What it does

- Trains a linear regression pipeline on temperature, rainfall, day of week, and month.
- Uses 70% of the CSV for training and 30% for evaluation.
- Serves a custom Flask website with a static HTML/CSS/JS frontend and JSON APIs.

## Run it

1. Install the dependencies:

   pip install -r requirements.txt

2. Train the model:

   python train_model.py

3. Start the website:

   python app.py

4. Open the local Flask address shown in the terminal.

## Files

- train_model.py trains and saves the regression model.
- app.py serves the website and handles API predictions.
- static/index.html contains the page layout.
- static/app.js handles API requests and dynamic rendering.
- static/style.css contains the custom UI.

## Deploy On Render

1. Push this project to GitHub.
2. Open Render and click New + -> Blueprint.
3. Connect your GitHub account and select this repository.
4. Render will detect render.yaml automatically.
5. Click Apply and wait for deploy to finish.

After deploy, Render gives you a public URL for the app.
