"""
DB から抽出した進捗履歴 CSV を整形し、プロジェクト単位で出力するツール。

主な処理：
- CSV の読み込み
- 「●」の最古のみ残すフィルタリング
- 日本語/英語カラムの両対応
- 出力フォルダの自動生成
- GUI（PySide6）による操作
"""

from datetime import datetime
import pandas as pd
import glob
import os
from .filters import filter_progress, filter_progress_jp


class ProgressExtractor:
    """進捗履歴 CSV の整形処理を担当するクラス"""

    def __init__(self, project_id: str, project_name: str):
        self.project_id = project_id
        self.project_name = project_name

    def run(self):
        """プロジェクトに紐づく CSV を整形して出力する"""
        today = datetime.now().strftime("%Y%m%d")
        base_dir = os.path.join(os.getcwd(), "抽出データ_PJID")
        out_dir = os.path.join(base_dir, f"{today}_{self.project_id}_{self.project_name}")

        os.makedirs(out_dir, exist_ok=True)

        # CSV 検索
        files = glob.glob("DBファイル/progressHistoryinfo_1/progress_ID_division/*.csv")
        hit_files = [f for f in files if self.project_name in os.path.basename(f)]

        if not hit_files:
            return None

        # 個別 CSV の整形
        for csv_file in hit_files:
            df = pd.read_csv(csv_file, encoding="utf-8")
            df["DateOf"] = pd.to_datetime(df["DateOf"], errors="coerce")

            # ● の最古のみ残す
            drop_idx = filter_progress(df)
            df = df.drop(drop_idx).reset_index(drop=True)

            # 保存
            out_name = os.path.basename(csv_file)
            df.to_csv(os.path.join(out_dir, out_name), index=False, encoding="utf-8-sig")

        # 統合処理（日本語版）
        merged = pd.concat(
            (pd.read_csv(f, encoding="utf-8-sig") for f in glob.glob(os.path.join(out_dir, "*.csv"))),
            ignore_index=True
        )
        merged["日付"] = pd.to_datetime(merged["日付"], errors="coerce")

        drop_idx2 = filter_progress_jp(merged)
        merged = merged.drop(drop_idx2).reset_index(drop=True)

        merged.to_csv(
            os.path.join(out_dir, f"{self.project_name}_integ.csv"),
            index=False,
            encoding="utf-8-sig"
        )

        return out_dir
