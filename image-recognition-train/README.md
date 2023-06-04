# 画像認識モデルのプロトタイプ: YOLOで物体検出

本リポジトリは，我々のサービス ___meguru___ において実際に画像認識モデルを導入し，カメラで撮影する画像データを用いて，新たに画像認識モデルを学習したり，学習済みモデルに追加で学習を行って精度を向上させたりするスキームのプロトタイプとして実装したものです．

本リポジトリでは一例として，[YOLOv5](https://github.com/ultralytics/yolov5)と転移学習を使って，固定カメラに映るベビーカー・スーツケース・車椅子を検知します．
[COCO128](https://cocodataset.org/)で学習済みのYOLOモデルの重みを初期値として，[Axross Recipe](https://axross-recipe.com/biz) DataHub (©SoftBank Corp.) 経由で提供された「[監視シーン下の物体識別データ](https://datahub.axross-recipe.com/datasets/2)」 (©Datatang Inc. ) を用いて追加で学習を実行します．



## Requirements
python >= 3.7

```
# 必要なパッケージのインストール
$ pip install -r requirements.txt
```

## Directory structure
※一部のデータや学習済みの重みは削除済み．

```
.
├── README.md
├── requirements.txt 
├── data.yaml  # 学習時の設定を記載
├── src
│   ├── mk_yolo_format_labels.py  # YOLO形式の学習データを作成
│   └── split_dataset.py  # 学習データを分割
├── training_result_object_in_scene  # DataHubデータで追加で学習を実行した結果
├── run-detect.sh 　# 学習済みのYOLOの実行例
├── sample  # YOLOの物体検出の実行結果の例
├── weights
│   ├── yolov5s.pt  # COCO128で学習済みの重み
│   └── yolov5s_additional_train_datahub_objects.pt  # DataHubデータで追加で学習を実行した重み
└── yolov5

```


## Usage

### **学習済みの重みを使用してYOLOで物体検出**
YOLOで物体検出をする実行例として，学習済みの重みを用いたインターフェースを[シェルスクリプト](run-detect.sh)として提供します．


```
$ run-detect.sh path/to/target
```
targetディレクトリ内に画像や動画ファイルがある場合，物体検出の結果が [sample/result/ ](./sample/result/) 内に保存されます．

スーツケースと本を対象とした物体検出の結果を [sample/ ](./sample/)に格納しています．


### **新しいデータを用いて(追加で)学習を行う手順** 
用意したデータを用いてYOLOモデルの学習を行う手順を説明します．
ここではDataHub「監視シーン下の物体識別データ」を用いる場合を例として説明します．

1. YOLO形式の学習データを作成 

「監視シーン下の物体識別データ」の場合を
[mk_yolo_format_labels.py ](./src/mk_yolo_format_labels.py)と [split_dataset.py](./src/split_dataset.py) に実装しています．
```
$ python mk_yolo_format_labels.py -t path/to/input  # YOLO形式の教師データに整形する
$ python split_dataset.py -t path/to/input -r example  # 学習データを分割する
``` 

2. 学習を実行

例えば，以下のように学習を実行します．
[data.yaml](data.yaml) ファイルに教師データのパスやクラス名を記載しておきます．
```
# 学習済みの重みを初期値として追加で学習する場合(こちらの結果を実行済み)
$ python yolov5/train.py --data data.yaml --weights yolov5s.pt --cfg yolov5s.yaml --batch-size 16  --epochs 100
```
```
# 初期値をランダムとして新しいデータを用いて学習を行う場合
$ python yolov5/train.py --data data.yaml --weights '' --cfg yolov5s.yaml  --batch-size 16 --epochs 100
```
