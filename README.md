# Medicinal Plant Recognition — ML Pipeline

Hybrid MobileNetV2 + ResNet50 feature-fusion model for classifying
medicinal plant leaf images.

## 1. Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Get a dataset (do this first — no dataset is bundled)

Recommended free options for fast turnaround:
- **Mendeley Medicinal Leaf Dataset** — search "Medicinal Leaf Dataset Mendeley"
- **Indian Medicinal Leaf Image Dataset** on Kaggle
- Or your own photographed leaves, if you want a dataset no other team is using
  (good for viva — examiners are wary of copy-pasted Kaggle projects)

Arrange it like this:

```
plant_recognition/
  dataset/
    Ashwagandha/
      img001.jpg
      img002.jpg
      ...
    Tulsi/
      img001.jpg
      ...
    Neem/
      ...
```

Aim for **at least 100–150 images per class** if possible; below ~50/class,
accuracy and the "≥90%" target in your synopsis get hard to hit honestly.
Fewer classes (10–15) with more images per class is a safer bet in two weeks
than many classes with thin data.

## 3. Train

```bash
python src/train.py
```

This runs two phases automatically:
1. Trains only the new classification head (backbones frozen) — fast.
2. Fine-tunes the top layers of both MobileNetV2 and ResNet50 — slower,
   improves accuracy.

Outputs land in `outputs/`:
- `hybrid_plant_model.keras` — the trained model
- `class_names.json` — index→label mapping (the backend needs this)
- `training_history.png` — accuracy/loss curves for your report

## 4. Evaluate

```bash
python src/evaluate.py
```

Produces `outputs/confusion_matrix.png` and `outputs/classification_report.txt`
(accuracy, precision, recall, F1 — overall and per-class). These go straight
into your "Expected Results" / experimental results chapter.

## 5. Test a single prediction (sanity check before backend integration)

```bash
python src/predict.py path/to/some_leaf.jpg
```

## Notes on realistic timeline (you have <2 weeks)

- **Don't** train from scratch multiple architectures to compare — you don't
  have time, and it's not needed to defend a hybrid design choice.
- Start Phase-1 training as soon as you have even a partial dataset (e.g. 5
  classes) to catch pipeline bugs early, then scale up classes once it's stable.
- If Colab/local GPU is slow, reduce `PHASE1_EPOCHS`/`PHASE2_EPOCHS` in
  `config.py` first — early stopping will end training early anyway once
  validation accuracy plateaus.
- Keep the confusion matrix and per-class report — examiners often ask
  "which classes did it confuse and why," and having a real answer (e.g.
  similar leaf shape/color) is worth more than a high accuracy number alone.
