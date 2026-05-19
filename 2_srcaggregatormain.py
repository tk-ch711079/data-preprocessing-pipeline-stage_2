"""
複数フォルダに分散した CSV を探索し、Excel に集約するツール。

主な処理：
- CSV の文字コード自動判定
- シート名の自動振り分け（接頭辞 → シート）
- 構造整理.xlsx によるヘッダー置換
- 機器工事情報 → 進捗情報 へのデータ転記
- 日付整形
"""

import os
import glob
import pandas as pd
from openpyxl import Workbook
from datetime import datetime
from .reader import read_csv_auto
from .header_mapper import apply_header_mapping
from .data_linker import link_equipment_info


class CsvAggregator:
    """CSV → Excel 集約処理を担当するクラス"""

    def __init__(self, project_id: str, project_name: str):
        self.project_id = project_id
        self.project_name = project_name

    def run(self):
        today = datetime.now().strftime("%Y%m%d")
        base_dir = os.path.join(os.getcwd(), "抽出データ_PJID")
        out_dir = os.path.join(base_dir, f"{today}_{self.project_id}_{self.project_name}")
        os.makedirs(out_dir, exist_ok=True)

        wb = Workbook()

        # シート作成
        sheet_map = {
            "CaI_": "カテゴリグループ",
            "ComI_": "会社情報",
            "EqiI_": "機器工事情報",
            "PI_": "進捗情報",
        }
        for name in sheet_map.values():
            wb.create_sheet(name)

        # CSV 探索
        for prefix, sheet_name in sheet_map.items():
            for csv_file in glob.glob(f"DBファイル/**/*{prefix}*.csv", recursive=True):
                df = read_csv_auto(csv_file)
                ws = wb[sheet_name]

                ws.append(list(df.columns))
                for row in df.itertuples(index=False, name=None):
                    ws.append(list(row))

        # ヘッダー置換
        apply_header_mapping(wb, "構造整理.xlsx")

        # 機器工事情報 → 進捗情報 転記
        link_equipment_info(wb)

        # 保存
        out_path = os.path.join(out_dir, f"{today}_{self.project_id}_{self.project_name}.xlsx")
        wb.save(out_path)

        return out_path
