# Nexmon環境構築手順 for RaspberryPi3/4B
ここでは，RaspberryPi3/4Bに**Nexmon**をインストールし，実際にCSIを取得するまでの一連の流れを説明します．

**Nexmon**：Cypress/Bloadcom製のWI-Fiチップ向けに開発された，オープンソースCSI収集用ファームウェアパッチです．

## RaspberryPiの初期設定
### イメージファイルの書き込み
- バージョン　　：Bullseye
- アーキテクチャ：armhf(ARM hard float)
- タイプ　　　　：Lite版
- リリース日　　：2022年1月28日
- ダウンロードURL：
https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2022-01-28/2022-01-28-raspios-bullseye-armhf-lite.zip

**Wi-Fi/SSHの設定**：この記事では詳しく触れませんが，各自設定していただくことを強く推奨します．

### 付録：公開鍵認証を使用したSSH接続
```
$ sudo apt update
$ cd ~
$ mkdir .ssh
$ touch .ssh/authorized_keys
$ nano .ssh/authorized_keys
// 自身の公開鍵（.pub）をコピペ
$ sudo reboot
```

## Nexmonのインストール
- Nexmon_csiのバイナリファイルから**インストールスクリプトを実行**（2分程度）

```
$ sudo curl -fsSL https://raw.githubusercontent.com/nexmonster/nexmon_csi_bin/main/install.sh | sudo bash
$ sudo reboot
```

※これ以降，**無線SSH接続ができなくなる**ため，有線SSH接続に切り替える

## CSI収集テスト
### 通信環境の確認
- **Wi-Fiアナライザ**などを使用して，観測したい無線通信チャネルと帯域幅を確認する

https://apps.microsoft.com/detail/9NBLGGH33N0N?hl=ja-JP&gl=JP

- mcpコマンドで，base64でエンコードされたパラメータ文字列を作成する

```
$ sudo mcp -C 1 -N 1 -c {チャネル}/{帯域幅}
```

※ここで**生成された文字列をコピー**しておくことを推奨

```
// mcpで指定できるオプションは-hで一覧表示可能
$ sudo mcp -h
```

### CSI収集開始
- パラメータ文字列を設定し，**モニターモードインターフェース(mon0)を追加**する

```
$ sudo ifconfig wlan0 up
$ sudo nexutil -Iwlan0 -s500 -b -l34 -{mcpで生成した文字列}
$ sudo iw dev wlan0 interface add mon0 type monitor
$ sudo ip link set mon0 up
```

- **tcpdumpコマンドでCSIの収集を開始**する

```
//基本的な実行コマンド
$ sudo tcpdump -i wlan0 dst port 5500

//書き込みファイルの指定
$ sudo tcpdump -i wlan0 dst port 5500 -vv -w {任意のファイル名}.pcap

//指定パケット数だけ書き込みファイルに出力
$ tcpdump -i wlan0 dst port 5500 -vv -w {任意のファイル名}.pcap -c {観測したいパケット数}

//例：1000パケットに達するまで観測し，output.pcapファイルとして出力する
$ sudo tcpdump -i wlan0 dst port 5500 -vv -w output.pcap -c 1000
```

※以降は，mon0インターフェースを追加する部分からコマンドを打ち込みなおす
