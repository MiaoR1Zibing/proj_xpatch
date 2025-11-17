import argparse
from docr.utils.file_utils import gen_random_str


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml', required=False,
                        help='Path to YAML config file. If provided, other arguments are ignored.')
    parser.add_argument('--model', default="unet", required=False,
                        help='Model name.')
    parser.add_argument('--gpu', type=int, nargs='+', default=[0], required=False,
                        help='Device id.')
    parser.add_argument('--log_folder', required=False,
                        help='Log folder.')
    parser.add_argument('--tag', default="{}".format(gen_random_str()), required=False,
                        help='Run identifier.')
    parser.add_argument('--patch_size', type=int, nargs='+', default=[512, 512], required=False,
                        help='patch size.')
    parser.add_argument('--batch_size', type=int, default=8, required=False,
                        help='batch size.')
    parser.add_argument('--initial_lr', type=float, default=1e-2, required=False,
                        help='initial learning rate.')
    parser.add_argument('--save_interval', type=int, default=25, required=False,
                        help='save_interval.')
    parser.add_argument('-c', '--continue_training', default=False, required=False, action='store_true',
                        help="restore from checkpoint and continue training.")
    parser.add_argument('--no_shuffle', default=False, required=False, action='store_true',
                        help="No shuffle training set.")
    parser.add_argument('--num_threads', type=int, default=4, required=False,
                        help="Threads number of dataloader.")
    parser.add_argument('-r', '--root', required=False,
                        help='dataset root folder.')
    parser.add_argument('--tr_csv', nargs='+',
                        required=False, help='training csv file.')
    parser.add_argument('--ts_csv', nargs='+',
                        required=False, help='test csv file.')
    parser.add_argument('--tu_csv', nargs='+',
                        required=False, help='unlabeled csv file.')
    parser.add_argument('--num_epochs', type=int, default=100, required=False,
                        help='num_epochs.')
    parser.add_argument('--beta', type=float, default=0.01, required=False,
                        help='beta in fourier.')  # fourier
    parser.add_argument('--rec_w', type=float, default=0.1, required=False,
                        help='High frequency reconstruction loss weight.')  # fourier

    args = parser.parse_args()
    if args.yaml:
        import yaml
        from argparse import Namespace

        # 保存原始的 yaml 配置文件路径（关键！）
        yaml_file_path = args.yaml  # 这里的 args 还是命令行解析的结果，包含 yaml 参数

        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as f:
                yaml_config = yaml.safe_load(f)

            args = Namespace(**yaml_config)  # 此时新的 args 覆盖了旧的，但我们已经保存了路径
            print(f"已从YAML配置文件加载参数：{yaml_file_path}")  # 用保存的路径打印
        except Exception as e:
            print(f"YAML配置加载失败：{str(e)}")
            return

    else:
        pass  # 原逻辑不变

    model_name = args.model

    if model_name == 'unet':
        from docr.training.train_nets.train_unet import train
    elif model_name == 'DoCR':
        from docr.training.train_nets.train_docr import train
    else:
        print('No model named "{}"!'.format(model_name))
        return
    train(args)


if __name__ == '__main__':
    main()
