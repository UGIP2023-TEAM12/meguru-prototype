# イベント参加者が利用するアプリのプロトタイプ: BLEアドバタイズのスキャン

本リポジトリは，我々のサービス ___meguru___ において，ユーザーが利用するIoTデバイスより発信されたビーコン（BLEアドバタイズ）を受信するアプリケーションをプロトタイプとして実装したものである．

ここでは一例として，ブラウザ上でハードウェア本体のBluetoothを利用できる技術である，[Web Bluetooth](https://github.com/WebBluetoothCG/web-bluetooth)を用いて，周囲のBLEアドバタイズをスキャンするWebアプリケーションを実装した．


## requirements

- Chromeを強く推奨
    - "chrome://flags/#enable-experimental-web-platform-features"をEnabledに
        - その他，ChromeへのBluetooth接続を許可する本体設定等が必要
    - Web Bluetoothは試験的な技術であるため，一部ハード上では正しく挙動しない可能性がある．
        - たとえば，iPhone等のiOS上では動作しない．
        - 各ハード，ブラウザの対応状況は[こちら](https://developer.mozilla.org/ja/docs/Web/API/Bluetooth)を参照されたい．

- python >= 3.10 (with poetry)
    - ローカルで動かす場合のみ
## Run locally
```
poetry install
poetry shell
uvicorn main:app --reload
```

Access "localhost:8000" in Chrome.

## Deployed App

Accsess [here](https://ble-receiver.onrender.com)

## Website
- /
    - 動作確認

- /index/?id=[hoge]
    - Web Bluetoothのスキャンをする．
    - ハードウェア名が[hoge]のアドバタイズを受信した時，alertがでる．