# Model Drift Detection System

Level: 11 — ML engineering

Skills: Python, a mean shift, a written threshold

Compare a current batch with a reference batch. Drift is true when the mean moves by at least two reference standard deviations. The check does not retrain a model.

```bash
pip install -r requirements.txt
pytest -q
```
