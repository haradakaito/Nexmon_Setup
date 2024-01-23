# Nexmon環境構築手順 for RaspberryPi3/4B
Nexmonは，Cypress/Bloadcom製のWI-Fiチップ向けに開発された，オープンソースCSI収集用ファームウェアパッチである．  
ここでは，RaspberryPi3/4BにNexmonをインストールし，実際にCSIを取得するまでの流れの一連を説明する． 

## 初期設定
### 起動設定
- [Nexmon対応のイメージ](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2022-01-28/2022-01-28-raspios-bullseye-armhf-lite.zip)を，[RasPi Imager](https://downloads.raspberrypi.org/imager/imager_latest.exe)でmicroSDに書き込む    
- microSDをRaspberryPiに差し込み，起動(HDMIを電源より先に挿入)
- (推奨)sudo raspi-configコマンドで[System Option]>[Boot/Auto Login]>[Yes]をしておくと次回以降自動でログイン  

### Wi-Fi接続設定
- 設定(etc)フォルダ下の，WPA認証ファイルをエディタで開く(以下，nanoエディタでの例)
```
$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
- 以下の文を，末尾に追記・保存して閉じる(""は必要)
```
network={
ssid="任意のSSID"
psk="パスワード"
key_mgmt=WPA-PSK
}
```
- Wi-Fiの内部ロックを外して無線LANの有効化したうえで再起動する
```
$ rfkill unblock wifi
$ sudo ifconfig wlan0 up
$ sudo reboot
```
ifconfigコマンドでwlan0の項目にIPアドレスが表示されていれば完了  

### SSH接続設定

## Nexmonのインストール

## CSI収集テスト
### 通信環境の確認

### CSI収集開始

### pcapファイルの復号

## 参考
Nexmon公式：https://github.com/seemoo-lab/nexmon  
Nexmonセットアップ(ホーム)：https://github.com/nexmonster/nexmon_csi  
Nexmonセットアップ(RasPi用)：https://github.com/nexmonster/nexmon_csi/tree/pi-5.10.92  

