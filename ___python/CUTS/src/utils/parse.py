import os
import sys
from pathlib import Path

# import_dir = '/'.join(os.path.realpath(__file__).split('/')[:-2])
# sys.path.insert(0, import_dir + '/utils/')
c_file = Path(__file__).resolve()
import_dir = c_file.parents[1]
sys.path.insert(0, str(import_dir / 'utils/'))

from attribute_hashmap import AttributeHashmap
from log_util import log


def parse_settings(config: AttributeHashmap, log_settings: bool = True):
    # fix typing issues
    config.learning_rate = float(config.learning_rate)
    config.weight_decay = float(config.weight_decay)

    # fix path issues
    # CUTS_ROOT = '/'.join(
    #     os.path.dirname(os.path.abspath(__file__)).split('/')[:-2])
    current_file = Path(__file__).resolve()  # 获取当前文件绝对路径（自动适配系统）
    CUTS_ROOT = current_file.parent.parent.parent  # 向上两级目录（等价于原逻辑的[:-2]）
    print('CUTS_ROOT', CUTS_ROOT)
    CUTS_ROOT = str(CUTS_ROOT)

    for key in config.keys():
        if type(config[key]) == str and '$CUTS_ROOT' in config[key]:
            config[key] = config[key].replace('$CUTS_ROOT', CUTS_ROOT)
        value = config[key]
        if isinstance(value, str) and (
                '/' in value or '\\' in value or  # 包含路径分隔符
                value.endswith(('.txt', '.csv', '.json', '')) or  # 常见文件后缀（可扩展）
                (len(value) > 1 and value[1] == ':')  # Windows盘符（如C:）
        ):
            # 转换为Path对象后再转为字符串，自动规范化路径格式
            config[key] = str(Path(value))

    # for ablation test
    if 'model_setting' in config.keys() and config.model_setting == 'no_recon':
        config.lambda_contrastive_loss = 1
    if 'model_setting' in config.keys() and config.model_setting == 'no_contrastive':
        config.lambda_contrastive_loss = 0

    # for "no label" option
    if 'no_label' not in config.keys():
        config.no_label = False

    # Initialize log file.
    # config.log_dir = config.log_folder + '/' + \
    #     os.path.basename(
    #         config.config_file_name).replace('.yaml', '') + '_log.txt'
    log_folder = Path(config.log_folder)
    config_file_basename = os.path.basename(config.config_file_name).replace('.yaml', '')
    log_filename = f"{config_file_basename}_log.txt"
    config.log_dir = str(log_folder / log_filename)

    if log_settings:
        log_str = 'Config: \n'
        for key in config.keys():
            log_str += '%s: %s\n' % (key, config[key])
        log_str += '\nTraining History:'
        log(log_str, filepath=config.log_dir, to_console=True)
    return config
