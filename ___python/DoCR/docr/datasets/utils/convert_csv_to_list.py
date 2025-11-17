from pathlib import Path

# def convert_labeled_list(csv_list, r=1):
#     img_pair_list = list()
#     for csv_file in csv_list:
#         with open(csv_file, 'r') as f:
#             img_in_csv = f.read().split('\n')[1:-1]
#         img_pair_list += img_in_csv
#     img_list = [i.split(',')[0] for i in img_pair_list]
#     if len(img_pair_list[0].split(',')) == 1:
#         label_list = None
#     else:
#         label_list = [i.split(',')[-1].replace('.tif', '-{}.tif'.format(r)) for i in img_pair_list]
#     return img_list, label_list

def convert_labeled_list(csv_list, r=1):
    img_pair_list = list()
    for csv_file in csv_list:
        # 将csv文件路径转换为Path对象（跨平台处理）
        csv_path = Path(csv_file)
        # 读取CSV文件（使用Path.open()方法，兼容跨平台路径）
        with csv_path.open('r') as f:
            # 读取所有行，跳过表头（[1:-1]去除空行和表头）
            img_in_csv = f.read().split('\n')[1:-1]
        img_pair_list += img_in_csv

    # 处理图像路径（转换为Path对象后再转为字符串，确保路径格式正确）
    img_list = [str(Path(i.split(',')[0])) for i in img_pair_list]

    # 处理标签路径（同样用Path处理）
    if len(img_pair_list[0].split(',')) == 1:
        label_list = None
    else:
        # 替换标签文件名中的.tif为-{r}.tif，并转换为跨平台路径
        label_paths = []
        for i in img_pair_list:
            original_label = i.split(',')[-1]
            # 替换文件名部分（保持路径结构不变）
            new_label = original_label.replace('.tif', f'-{r}.tif')
            # 转换为Path对象后再转字符串，自动适配平台分隔符
            label_paths.append(str(Path(new_label)))
        label_list = label_paths

    return img_list, label_list
