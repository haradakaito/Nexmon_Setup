from lib._csichanger import InputParser, OutputFormatter, Decoder

# CSIデータの処理
def decode_pcap2csv(filename: str, bandwidth: str, command: str) -> bool:
    """CSIデータ(.pcap)をCSVファイルに変換する"""
    try:
        print('Start Parsing input parameters...')
        # 入力パラメータの解析
        inputparser = InputParser(filename, bandwidth, command)
        if not inputparser.is_valid():
            print("\nError: Invalid input parameters.")
            print("1. Is the filename correct? (No extensions are needed)")
            print("2. Does the specified file exist under the 'pcapfiles' directory?")
            print("3. Is the bandwidth set to one of the valid values? (20, 40, 80, 160)")
            print("4. Is the command format 'number-number'?")
            return False
        params = inputparser.get_params()

        print('Start decoding...')
        # RSSIデータ処理
        decoder = Decoder(params['filepath'], params['command']['start'], params['command']['end'])
        amp_list = decoder.decode()

        print('Start outputting to CSV file...')
        # CSVファイル出力
        outputformatter = OutputFormatter(params['filename'])
        outputformatter.to_csv(amp_list)
        return True
    except Exception as e:
        print(e)
        return False

# テスト用
if __name__ == '__main__':
    decode_pcap2csv(filename='sample', bandwidth='20', command='0-10')