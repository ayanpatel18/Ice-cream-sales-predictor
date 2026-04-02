# Product Requirements Document: Ice Cream Sales Predictor

## 1. Overview

Build a web-based ice cream sales predictor that uses the `ice-cream.csv` dataset to estimate future sales from weather and calendar inputs. The product will train a regression model, validate it with a 70/30 train-test split, and expose predictions through a Flask-powered user interface.

## 2. Product Goal

Provide a simple but distinctive forecasting tool that helps users estimate ice cream demand before a given day using temperature, rainfall, day of week, and month.

## 3. Success Criteria

- The model trains successfully on `ice-cream.csv`.
- The dataset is split into 70% training and 30% validation/testing.
- A regression model, specifically linear regression, is used as the baseline algorithm.
- The app returns a numeric sales forecast from the Flask UI.
- The interface feels custom and polished rather than like a default template.

## 4. Users

- Small business owners tracking daily ice cream demand.
- Students or portfolio reviewers evaluating a machine learning web app.
- Developers who want a simple predictive dashboard.

## 5. Data Requirements

### Source

- File: `ice-cream.csv`

### Expected Columns

- `Date`
- `DayOfWeek`
- `Month`
- `Temperature`
- `Rainfall`
- `IceCreamsSold`

### Data Usage

- `IceCreamsSold` is the target variable.
- `Temperature`, `Rainfall`, `DayOfWeek`, and `Month` are used as model inputs.
- `Date` may be parsed to derive day-of-week and month if needed.

## 6. Model Requirements

### Algorithm

- Use linear regression as the primary model.

### Validation

- Split the dataset into 70% training and 30% validation/test data.
- Report validation metrics after training.

### Metrics

- R2 score
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

### Model Behavior

- The model should accept weather and date-based inputs.
- The model should output a predicted number of ice creams sold.
- Predicted values should be displayed as non-negative numbers.

## 7. Application Requirements

### Backend

- Use Flask as the web server.
- Load the trained model from disk.
- Accept form submissions for forecast inputs.
- Generate predictions on request.

### Frontend

- Build a custom user interface with a strong visual identity.
- Include:
  - Input fields for date, temperature, and rainfall
  - A prediction button
  - A visible prediction result area
  - A compact metrics section
  - A short explanation of how the model works

## 8. Core User Flow

1. User opens the homepage.
2. User enters a date, temperature, and rainfall amount.
3. User submits the form.
4. Flask converts the date into model-friendly features.
5. The linear regression model returns a sales forecast.
6. The prediction is shown on the page.

## 9. Non-Functional Requirements

- Fast local inference.
- Responsive layout for desktop and mobile.
- Clear error handling for invalid inputs.
- Reproducible training with a fixed random state.
- Minimal external dependencies.

## 10. Architecture

### Training Script

- Reads `ice-cream.csv`.
- Prepares features.
- Splits data into 70/30 training and validation sets.
- Trains a linear regression pipeline.
- Saves the trained model artifact.

### Flask App

- Loads the saved model.
- Serves the prediction UI.
- Handles prediction requests.
- Displays evaluation summary and predictions.

## 11. Deliverables

- Trained regression model artifact
- Flask application
- Custom HTML/CSS user interface
- Documentation for setup and execution

## 12. Out of Scope

- User authentication
- Cloud deployment
- Multi-model comparison dashboard
- Automated retraining pipeline
- Real-time weather API integration

## 13. Risks and Assumptions

- The CSV may be small, so model performance should be interpreted conservatively.
- Linear regression is chosen for simplicity and interpretability, not maximum predictive power.
- Historical sales patterns may not fully generalize to future weather conditions.

## 14. Acceptance Criteria

- The model trains without errors using the provided CSV.
- Validation uses a 70/30 split.
- The Flask UI submits inputs and returns a prediction successfully.
- The page has a custom design that is visibly distinct from a default Flask template.
- Metrics are visible to the user or easy to inspect from the app output.

## 15. Suggested Implementation Plan

- Step 1: Load and inspect the CSV.
- Step 2: Prepare features and target values.
- Step 3: Train and validate a linear regression pipeline.
- Step 4: Save the trained model and metrics.
- Step 5: Build the Flask UI.
- Step 6: Wire the form to the prediction endpoint.
- Step 7: Test the full flow end to end.
