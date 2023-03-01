# ビーコンのプロトタイプ: YOLOで物体検出し，BLEを発信

## 概要
本パッケージは，我々のサービス ___meguru___ において，カメラ撮影する動画に対して，リアルタイムで物体検出を行い，対象の物体が検出された場合，信号を発信するビーコンのプロトタイプとして実装したものです．

本パッケージでは，シングルボードコンピューター [Raspberry Pi](https://www.raspberrypi.com/) とカメラを用いて，[YOLOv5](https://github.com/ultralytics/yolov5) による物体検出を行い，[bluez](http://www.bluez.org/) を用いて BLE (Bluetooth Low Energy) を発信しています．

物体検出において，学習済みの重みを`meguru-prototype/beacon-sender/weights` 下に配置することで，推論に使用できます．物体検出の結果は，`meguru-prototype/beacon-sender/data` に保存されます．

## Usage
### `bluez-5.9` と `bluez-ibeacon` のコンパイル
```
cd bluez-5.9
./configure --disable-systemd --enable-library
make
make install
```

```
cd ./bluez-ibeacon/bluez-beacon/
make
```

### UUIDの生成
```
uuidgen
```

### 実行
```
python src/emit_beacon_when_detecting_objects.py --weight_nm (学習済みの重みファイル名) --uuid (UUID) --target_object (対象物体のクラス名)
```

## Requirements
- libusb-dev
- libdbus-1-dev
- libglib2.0-dev
- libudev-dev
- libical-dev
- libreadline-dev
- libdbus-glib-1-dev
- libbluetooth-dev
- uuid-runtime
- [ultralytics/yolov5/requirements.txt](https://github.com/ultralytics/yolov5/blob/master/requirements.txt)