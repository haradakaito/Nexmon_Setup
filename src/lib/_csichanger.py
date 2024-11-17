import os
import numpy as np
import pandas as pd
import importlib
from config import config

# 定数
PCAP_EXTENTION = '.pcap'
CSV_DIR        = './result'
DECODER_DIR    = 'lib'

class InputParser:
    def __init__(self, filename: str, bandwidth: str, command: str) -> None:
        self.filename  = filename
        self.bandwidth = bandwidth
        self.command   = command

    def get_params(self) -> dict:
        filename    = self.filename
        bandwidth   = float(self.bandwidth)
        nsub        = int(bandwidth * 3.2)
        columns_amp = np.arange(-1 * nsub/2, nsub/2)
        start, end  = map(int, self.command.split('-'))
        filepath    = os.path.join(config.pcap_fileroot, filename + PCAP_EXTENTION)
        return {
            'filename'    : filename,
            'bandwidth'   : bandwidth,
            'columns_amp' : columns_amp,
            'command'     : {'start': start, 'end': end},
            'filepath'    : filepath
        }

    def is_valid(self) -> bool:
        return all([
            self._is_filename_valid(),
            self._is_file_exists(),
            self._is_bandwidth_valid(),
            self._is_command_valid()
        ])

    def _is_filename_valid(self) -> bool:
        return PCAP_EXTENTION not in self.filename

    def _is_file_exists(self) -> bool:
        fileroot = config.pcap_fileroot
        return os.path.exists(os.path.join(fileroot, self.filename + PCAP_EXTENTION))

    def _is_bandwidth_valid(self) -> bool:
        return self.bandwidth in config.bandwidths

    def _is_command_valid(self) -> bool:
        if '-' in self.command:
            start, end = self.command.split('-')
            return start.isnumeric() and end.isnumeric()
        return False

class OutputFormatter:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def to_csv(self, data: list) -> None:
        if not self._is_directory_exists():
            os.makedirs(CSV_DIR)
        df = pd.DataFrame(data)
        df.to_csv(f'{CSV_DIR}/{self.filename}.csv')

    def _is_directory_exists(self) -> bool:
        return os.path.exists(CSV_DIR)

class Decoder:
    def __init__(self, filepath, start, end) -> None:
        self.decoder  = importlib.import_module(f'{DECODER_DIR}.{config.decoder}')
        self.filepath = filepath
        self.start    = start
        self.end      = end

    def decode(self) -> object:
        samples = self.decoder.read_pcap(self.filepath)
        # RSSIデータ処理
        amp_list = [
            np.abs(
                samples.get_csi(
                    index,
                    config.remove_null_subcarriers,
                    config.remove_pilot_subcarriers
                )
            )
            for index in range(self.start, self.end+1)
        ]
        return amp_list