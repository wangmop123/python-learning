# Lung Cancer Classification Django Project

This is a complete Django project for your lung cancer classification notebook.

What this project includes:
- training script to create the model artifact
- Django web app with form input for all features
- prediction page
- production settings ready for deployment
- clean folder structure

## 1. Create virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

## 2. Install packages

```bash
pip install -r requirements.txt
```

## 3. Put your dataset in the project root

Place this file in the root folder:
`survey_lung_cancer.csv`

## 4. Train the model

```bash
python train_model.py
```

This will create:
`predictor/ml/lung_cancer_artifacts.pkl`

## 5. Run migrations

```bash
python manage.py migrate
```

## 6. Start server

```bash
python manage.py runserver
```

Open:
http://127.0.0.1:8000/

## 7. Deploy

For production:
```bash
python manage.py collectstatic --noinput
gunicorn lung_project.wsgi
```

## Dataset columns expected

- GENDER
- AGE
- SMOKING
- YELLOW_FINGERS
- ANXIETY
- PEER_PRESSURE
- CHRONIC DISEASE
- FATIGUE
- ALLERGY
- WHEEZING
- ALCOHOL CONSUMING
- COUGHING
- SHORTNESS OF BREATH
- SWALLOWING DIFFICULTY
- CHEST PAIN
- LUNG_CANCER

## Notes

- GENDER accepts M or F
- The symptom fields use 1 or 2, based on your dataset
- Target output is YES or NO
