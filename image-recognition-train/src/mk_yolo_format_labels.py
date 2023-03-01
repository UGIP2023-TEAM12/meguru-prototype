"""ラベルを YOLO format に変換"""
import argparse
import glob
import json
import os
from typing import Any, Dict, List


def read_args() -> argparse.Namespace:
    """引数の読み込み"""
    parser = argparse.ArgumentParser(description="yolov5の学習データを分割する")
    parser.add_argument(
        "-t",
        "--target_dir",
        type=str,
        help="Input data dir",
    )
    parser.add_argument(
        "-w",
        "--width",
        default=1920,
        type=int,
        help="Image size width",
    )
    parser.add_argument(
        "-h",
        "--height",
        default=1080,
        type=int,
        help="Image size height",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # 引数の読み込み
    args = read_args()

    # ファイルパスの一覧を取得
    labels_paths: List[str] = sorted(glob.glob(args.target_dir + "*.json"))

    for json_file_path in labels_paths:
        json_items: Dict[str, Any] = json.load(open(json_file_path, "r"))
        coordinates: List[List[float]] = json_items["coordinates"]  # バウンディングボックスの座標

        # YOLO format に必要な値の計算
        x_center: float = ((coordinates[0][0] + coordinates[1][0]) / 2) / args.width
        y_center: float = ((coordinates[0][1] + coordinates[2][1]) / 2) / args.height
        width: float = (coordinates[1][0] - coordinates[0][0]) / args.width
        height: float = (coordinates[2][1] - coordinates[0][1]) / args.height

        # format 変換後のファイルパスを作成
        dirname: str = os.path.dirname(json_file_path)
        basename_without_ext: str = os.path.splitext(os.path.basename(json_file_path))[0]
        target_file_path: str = dirname + "/" + basename_without_ext + ".txt"

        # ファイルへ書き込み
        with open(target_file_path, "w") as f:
            f.write(f"0\t{x_center}\t{y_center}\t{width}\t{height}")
