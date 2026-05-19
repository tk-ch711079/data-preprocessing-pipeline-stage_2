# Data Preprocessing Pipeline (Stage 2)

本リポジトリは、業務システムから抽出された進捗データを
「整形 → 集約 → Excel 後処理」するための前処理パイプライン（Stage2）をまとめたものです。

Stage1 で抽出・分割された CSV を入力として、
プロジェクト単位での進捗データ整形、複数フォルダに分散した CSV の Excel 集約、
および名称埋め込み・不要列削除などの後処理を自動化します。

数百万レコード規模のデータを扱うことを前提に設計しており、
pandas / openpyxl / PySide6 を組み合わせて、
業務で利用可能なレベルのデータ整形パイプラインを構築しています。

---

## 📌 Stage2 の構成

### **1. ProgressExtractor（進捗 CSV 整形）**
- プロジェクト名に紐づく CSV を検索
- 「●」の最古のみ残すフィルタリング
- 日本語版カラムの統合
- プロジェクト単位のフォルダへ出力  
- `progress_extractor.py`

### **2. CsvAggregator（CSV → Excel 集約）**
- 複数フォルダに分散した CSV を探索
- 接頭辞（CaI_ / ComI_ / EqiI_ / PI_）に応じてシート振り分け
- 構造整理.xlsx によるヘッダー置換
- 機器工事情報 → 進捗情報 のデータ転記
- Excel 形式で出力  
- `csv_aggregator.py`

### **3. ProgressPostProcessor（Excel 後処理）**
- CSV を「進捗履歴情報」シートへ貼り付け
- マスタシート（カテゴリ / 会社）の辞書化
- 名称埋め込み（カテゴリ名・会社名）
- 不要列削除  
- `progress_post_processor.py`

---

## 🛠 使用技術
- Python 3.x
- pandas
- openpyxl
- PySide6

---

## 📄 ライセンス
本リポジトリは転職用のサンプルとして公開しています。  
実際の業務データ・接続情報は含まれていません。


