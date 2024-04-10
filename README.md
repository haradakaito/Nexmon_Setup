# Nexmon環境構築手順 for RaspberryPi3/4B
Nexmonは，Cypress/Bloadcom製のWI-Fiチップ向けに開発された，**オープンソースCSI収集用ファームウェアパッチ**です．
ここでは，**RaspberryPi3/4BにNexmonをインストール**し，実際にCSIを取得するまでの一連の流れを説明します．

## 0. 初期設定
ここでは，Nexmonの環境構築を行うにあたって，**Wi-Fi/SSH設定を行います**．
※RaspberryPiのSDカードにイメージファイルを書き込む段階で，設定ファイルを編集して各種設定を行う方が簡単だと思います．
### 0.1. 起動設定
- [Nexmon対応のイメージ](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2022-01-28/2022-01-28-raspios-bullseye-armhf-lite.zip)を，[RasPi Imager](https://downloads.raspberrypi.org/imager/imager_latest.exe)でmicroSDに書き込む    
- microSDをRaspberryPiに差し込み，起動(HDMIを電源より先に挿入)
- (推奨)sudo raspi-configコマンドで[System Option]>[Boot/Auto Login]>[Yes]をしておくと次回以降自動でログイン  

### 0.2. Wi-Fi接続設定
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
- ifconfigコマンドでwlan0の項目にIPアドレスが表示されていれば完了  

### 0.3. SSH接続設定
- SSH接続を有効にする
sudo raspi-configコマンドで[Interfacing Options]>[SSH]>[Yes]を選択  
- RaspberryPiのIPアドレスを確認する
ipconfigコマンドでwlan0に記載のIPアドレスを確認(記録)しておく
- SSH接続を行うデバイスで，PowerShellを管理者権限で起動
```
$ ssh pi@XXX.XXX.XXX.XXX  #先ほど確認したIPアドレスを入力
```
## 1. Nexmonのインストール
- Nexmon_csiのバイナリファイルから**インストールスクリプトを実行**(目安：2分)
```
$ sudo curl -fsSL https://raw.githubusercontent.com/nexmonster/nexmon_csi_bin/main/install.sh | sudo bash
$ sudo reboot
```
※**これ以降，無線SSH接続ができなくなる**ため，有線SSH接続に切り替える  

## 2. CSI収集テスト
### 2.1. 通信環境の確認
- [Wi-Fiアナライザ](https://apps.microsoft.com/detail/9NBLGGH33N0N?hl=ja-JP&gl=JP)などで**観測したい無線通信のチャネルと帯域幅などを確認**する
- mcpコマンドで，base64でエンコードされたパラメータ文字列を作成する
- 出力された**文字列を確認(記録)する**
```
$ sudo mcp -C 1 -N 1 -c チャネル/帯域幅
```
mcpコマンドで指定できるオプション一覧は-hで表示できる．
```
$ sudo mcp -h
```
### 2.2. CSI収集開始
- 観測パラメータ文字列を設定し，**モニターモードインターフェース(mon0)を追加**する
```
$ sudo ifconfig wlan0 up
$ sudo nexutil –Iwlan0 –Iwlan0 –s500 –b –l34 –v [mcpで生成したパラメータ文字列]
$ sudo iw dev wlan0 interface add mon0 type monitor
$ sudo ip link set mon0 up
```
- **tcpdumpコマンドでCSIの収集を開始**する
※ 例)1000パケットに達するまで観測し，output.pcapファイルとして出力する  
```
$ sudo tcpdump –i wlan0 dst port 5500 –vv –w output.pcap –c 1000
```
次回からは，モニターモードインターフェースを追加するところから始めればいい

### 2.3. pcapファイルの復号
ここでは，**僕が自作したプログラムを用いてpcapファイルからCSI情報をcsvファイルに抽出するプログラムの使い方を解説**する．pcapファイルの復号方法が独自である場合は，見る必要はないです．
- [WinSCP](https://winscp.net/eng/download.php)などを使用して，RaspberryPiからpcapファイルをダウンロードする
- 「csi_changer」フォルダ内の「pcapfiles」フォルダに復号したいpcapファイルを置く
- csi_changer.pyを起動する
```
$ python csi_changer.py
```
- 「pcapファイル名」と「帯域幅」を入力
```
$ python csi_changer.py
Pcap File Name: XXX
Band Width: YYY
```
- resultフォルダ内に「XXX_CSI_Amp.csv」と「XXX_CSI_Pha.csv」が出力されていれば完了

## Qitta記事
https://qiita.com/muumin_0525/items/8e9ef1081b372509d4a1
