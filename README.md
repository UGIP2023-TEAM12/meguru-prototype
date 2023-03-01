# [meguru-prototype](https://github.com/UGIP2023-TEAM12/meguru-prototype)

我々のサービス ___meguru___ は大きく以下の3プロセスで構成される．

1. イベント参加者の所有品をIoTデバイスが物体検出
2. 当該のアイテムを検出すると，IoTデバイスよりビーコン(BLE)が発信される
3. イベント参加者のスマートフォンで，発信されたビーコンを受信する

<img src="https://user-images.githubusercontent.com/80742820/222148869-1635adda-e899-47f4-a04e-c0127b6d89e7.png" >

実際の流れは[紹介動画](https://axross-recipe.com/recipes/866)を閲覧されたい．


以上のプロセスを実現するため，プロトタイプとして以下の3システムを試験的に実装した．
1. 画像認識モデルの学習 [image-recognition-train](https://github.com/UGIP2023-TEAM12/meguru-prototype/tree/main/image-recognition-train)
2. ビーコンの発信装置 [beacon-sender](https://github.com/UGIP2023-TEAM12/meguru-prototype/tree/main/beacon-sender)
3. ビーコンを受信するアプリケーション [beacon-receiver](https://github.com/UGIP2023-TEAM12/meguru-prototype/tree/main/beacon-receiver)

下にその概略を説明する．より具体的な実装の詳細や，利用方法は各レポジトリを参照されたい．

## image-recognition-train

実際に画像認識モデルを導入し，カメラで撮影する画像データを用いて，新たに画像認識モデルを学習したり，学習済みモデルに追加で学習を行って精度を向上させたりするスキームのプロトタイプとして実装したもの．

一例として，[YOLOv5](https://github.com/ultralytics/yolov5)と転移学習を使い，固定カメラに映るベビーカー・スーツケース・車椅子を検知する．
[COCO128](https://cocodataset.org/)で学習済みのYOLOモデルの重みを初期値として，[Axross Recipe](https://axross-recipe.com/biz) DataHub (©SoftBank Corp.) 経由で提供された「[監視シーン下の物体識別データ](https://datahub.axross-recipe.com/datasets/2)」 (©Datatang Inc. ) を用いて追加で学習を実行した．．

## beacon-sender

カメラ撮影する動画に対して，リアルタイムで物体検出を行い，対象の物体が検出された場合，信号を発信するビーコンのプロトタイプとして実装したもの．

シングルボードコンピューター [Raspberry Pi](https://www.raspberrypi.com/) とカメラを用い，[YOLOv5](https://github.com/ultralytics/yolov5) による物体検出を行い，[bluez](http://www.bluez.org/) を用いてBLE (Bluetooth Low Energy) を発信する．

また，物体検出において，学習済みの重みをimage-recognition-trainシステムで得られた学習済みの重みを推論に使用できる．

## beacon-receiver

ユーザーが利用する，IoTデバイスより発信されたビーコン（BLEアドバタイズ）を受信するアプリケーションをプロトタイプとして実装したもの．

ここでは一例として，ブラウザ上でハードウェア本体のBluetoothを利用できる技術である，[Web Bluetooth](https://github.com/WebBluetoothCG/web-bluetooth)を用いて，周囲のBLEアドバタイズをスキャンするWebアプリケーションを実装した．

特定のビーコンを受信すると，自動でユーザーにそのことが通知される．
