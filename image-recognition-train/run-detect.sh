#!/bin/bash
# 学習済みの YOLO の実行例
# 引数で実行対象のファイル/ディレクトリを指定する

# COCO128(オープンデータ)で学習済みの重みを使用する場合
python yolov5/detect.py --weights weights/yolov5s.pt --img 640 --conf-thres 0.25 --source $@ 

# Datahubデータセットで追加で学習済みの重みを使用する場合
# python yolov5/detect.py --weights weights/yolov5s_additional_train_datahub_objects.pt --img 640 --conf-thres 0.25 --source $@ 

# ディレクトリ直下にデータを保存する
mv yolov5/runs/detect/exp/* ./sample/result/
rm -r yolov5/runs/detect/exp/