#!/usr/bin/env python3
"""Entrena el modelo IDS basado en el pipeline de clases/CiberTelepatia."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.preprocessing import StandardScaler

TRAIN_URL = 'https://raw.githubusercontent.com/jmnwong/NSL-KDD-Dataset/master/KDDTrain%2B.txt'
TEST_URL = 'https://raw.githubusercontent.com/jmnwong/NSL-KDD-Dataset/master/KDDTest%2B.txt'
COLUMN_NAMES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate', 'attack', 'difficulty'
]


def load_dataset(train_url: str, test_url: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_df = pd.read_csv(train_url, names=COLUMN_NAMES, header=None)
    test_df = pd.read_csv(test_url, names=COLUMN_NAMES, header=None)
    return train_df, test_df


def preprocess(train_df: pd.DataFrame, test_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    train_df = train_df.copy()
    test_df = test_df.copy()
    train_df['is_attack'] = (train_df['attack'] != 'normal').astype(int)
    test_df['is_attack'] = (test_df['attack'] != 'normal').astype(int)
    train_df.drop(columns=['attack', 'difficulty'], inplace=True)
    test_df.drop(columns=['attack', 'difficulty'], inplace=True)

    cat_cols = ['protocol_type', 'service', 'flag']
    train_proc = pd.get_dummies(train_df, columns=cat_cols)
    test_proc = pd.get_dummies(test_df, columns=cat_cols)

    missing_cols = set(train_proc.columns) - set(test_proc.columns)
    for col in missing_cols:
        test_proc[col] = 0
    extra_cols = set(test_proc.columns) - set(train_proc.columns)
    if extra_cols:
        test_proc.drop(columns=list(extra_cols), inplace=True)
    test_proc = test_proc[train_proc.columns]

    y_train = train_proc['is_attack']
    X_train = train_proc.drop(columns=['is_attack'])
    y_test = test_proc['is_attack']
    X_test = test_proc.drop(columns=['is_attack'])

    numeric = [c for c in X_train.columns if not c.startswith(('protocol_type_', 'service_', 'flag_'))]
    scaler = StandardScaler(with_mean=False)
    X_train[numeric] = scaler.fit_transform(X_train[numeric])
    X_test[numeric] = scaler.transform(X_test[numeric])

    return X_train, y_train, X_test, y_test


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    clf = RandomForestClassifier(
        n_estimators=200,
        n_jobs=-1,
        random_state=42,
        class_weight='balanced',
    )
    clf.fit(X_train, y_train)
    return clf


def evaluate(clf: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    preds = clf.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    report = classification_report(y_test, preds, target_names=['Normal', 'Attack'])
    return {
        'accuracy': accuracy,
        'f1': f1,
        'classification_report': report,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Train IDS model (NSL-KDD)')
    parser.add_argument('--output', default='proyecto_integrado/services/ids-ml/models/best_model.joblib')
    parser.add_argument('--metadata', default='proyecto_integrado/services/ids-ml/models/model_metadata.json')
    args = parser.parse_args()

    print('Descargando dataset...')
    train_df, test_df = load_dataset(TRAIN_URL, TEST_URL)
    print('Preprocesando...')
    X_train, y_train, X_test, y_test = preprocess(train_df, test_df)
    print('Entrenando RandomForest...')
    clf = train_model(X_train, y_train)
    print('Evaluando...')
    metrics = evaluate(clf, X_test, y_test)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, out_path)
    print(f'Modelo guardado en {out_path}')
    metadata = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'train_url': TRAIN_URL,
        'test_url': TEST_URL,
        'accuracy': metrics['accuracy'],
        'f1': metrics['f1'],
    }
    Path(args.metadata).write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    (out_path.parent / 'evaluation.txt').write_text(metrics['classification_report'], encoding='utf-8')
    print('Métricas:', json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
