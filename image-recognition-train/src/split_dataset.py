"""yolov5の学習-検証-テストデータを作成"""

import argparse
import glob
import os
import random
import shutil
from typing import List, Tuple


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
        "-r",
        "--result_dir",
        type=str,
        help="Output dir",
    )
    return parser.parse_args()


def move_files(file_list: List[str], target_dir: str) -> None:
    """一括でファイルを移動

    Args:
        file_list: images/labels ファイルパスのリスト
        target_dir: 移動先のディレクトリ
    """
    for file in file_list:
        shutil.copy(file, target_dir)


if __name__ == "__main__":
    # 引数の読み込み
    args = read_args()

    # ファイルパスの一覧を取得
    images_paths: List[str] = sorted(glob.glob(args.target_dir + "*.bmp"))
    labels_paths: List[str] = sorted(glob.glob(args.target_dir + "*.txt"))

    # シャッフル
    _temp: List[Tuple[str, str]] = list(zip(images_paths, labels_paths))
    random.shuffle(_temp)
    images_paths, labels_paths = list(map(list, list(zip(*_temp))))

    # ファイルを分割(train, val, test)
    idx_test_start: int = int(len(images_paths) * 0.8)
    idx_val_start: int = int(idx_test_start * 0.8)

    images_train = images_paths[:idx_val_start]
    labels_train = labels_paths[:idx_val_start]

    images_valid = images_paths[idx_val_start:idx_test_start]
    labels_valid = labels_paths[idx_val_start:idx_test_start]

    images_test = images_paths[idx_test_start:]
    labels_test = labels_paths[idx_test_start:]

    # train/valid/test用のディレクトリを作成
    os.makedirs(f"../yolov5/data/{args.result_dir}/train/images", exist_ok=True)
    os.makedirs(f"../yolov5/data/{args.result_dir}/train/labels", exist_ok=True)

    os.makedirs(f"../yolov5/data/{args.result_dir}/valid/images", exist_ok=True)
    os.makedirs(f"../yolov5/data/{args.result_dir}/valid/labels", exist_ok=True)

    os.makedirs(f"../yolov5/data/{args.result_dir}/test/images", exist_ok=True)
    os.makedirs(f"../yolov5/data/{args.result_dir}/test/labels", exist_ok=True)

    # ファイル移動
    move_files(images_train, f"../yolov5/data/{args.result_dir}/train/images")
    move_files(labels_train, f"../yolov5/data/{args.result_dir}/train/labels")

    move_files(images_valid, f"../yolov5/data/{args.result_dir}/valid/images")
    move_files(labels_valid, f"../yolov5/data/{args.result_dir}/valid/labels")

    move_files(images_test, f"../yolov5/data/{args.result_dir}/test/images")
    move_files(labels_test, f"../yolov5/data/{args.result_dir}/test/labels")
