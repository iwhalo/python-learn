import json
import os


def check_duplicate_floors_from_file(file_path):
    """
    从JSON文件检查edifice数组中是否有重复的floor值

    Args:
        file_path: JSON文件路径

    Returns:
        dict: 包含检查结果的信息
    """
    print(f"正在检查文件: {file_path}")
    print("=" * 60)

    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return {
                'has_duplicates': False,
                'message': f'文件不存在: {file_path}',
                'error': True,
                'file_exists': False
            }

        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 获取edifice数组
        edifice = data.get('data', {}).get('edifice', [])

        if not edifice:
            return {
                'has_duplicates': False,
                'message': 'edifice数组为空',
                'duplicates': {},
                'total_count': 0,
                'unique_count': 0
            }

        print(f"edifice数组长度: {len(edifice)}")

        # 提取所有floor值
        floors = []
        floor_details = {}  # 记录每个floor的详细信息

        for i, item in enumerate(edifice):
            if 'floor' in item:
                floor_value = item['floor']
                floors.append(floor_value)

                # 记录详细信息
                if floor_value not in floor_details:
                    floor_details[floor_value] = []
                floor_details[floor_value].append({
                    'index': i,
                    'uid': item.get('uid'),
                    'nick': item.get('nick'),
                    'avatar': item.get('avatar'),
                    'mf': item.get('mf')
                })

        print(f"提取的floor值数量: {len(floors)}")

        # 统计每个floor值出现的次数
        floor_count = {}
        for floor in floors:
            if floor in floor_count:
                floor_count[floor] += 1
            else:
                floor_count[floor] = 1

        # 找出重复的floor值
        duplicates = {floor: count for floor, count in floor_count.items() if count > 1}

        has_duplicates = len(duplicates) > 0

        result = {
            'has_duplicates': has_duplicates,
            'total_count': len(floors),
            'unique_count': len(set(floors)),
            'duplicates': duplicates,
            'duplicate_count': len(duplicates),
            'floor_details': floor_details,
            'file_exists': True
        }

        if has_duplicates:
            result['message'] = f'发现 {len(duplicates)} 个重复的floor值'
        else:
            result['message'] = '没有发现重复的floor值'

        return result

    except json.JSONDecodeError as e:
        return {
            'has_duplicates': False,
            'message': f'JSON解析错误: {str(e)}',
            'error': True,
            'file_exists': True
        }
    except Exception as e:
        return {
            'has_duplicates': False,
            'message': f'处理数据时发生错误: {str(e)}',
            'error': True,
            'file_exists': True
        }


def print_detailed_results(result):
    """
    打印详细的检查结果

    Args:
        result: check_duplicate_floors_from_file函数的返回结果
    """
    print(f"状态: {result['message']}")
    print(f"总记录数: {result.get('total_count', 0)}")
    print(f"唯一楼层数: {result.get('unique_count', 0)}")

    if result.get('has_duplicates', False):
        duplicates = result.get('duplicates', {})
        print(f"\n重复的楼层值 ({result.get('duplicate_count', 0)}个):")
        print("-" * 60)

        # 按楼层号排序输出
        for floor in sorted(duplicates.keys()):
            count = duplicates[floor]
            print(f"  楼层 {floor}: 出现 {count} 次")

        # 显示重复楼层的详细信息
        print("\n重复楼层的详细信息:")
        print("-" * 60)

        floor_details = result.get('floor_details', {})
        for floor in sorted(duplicates.keys()):
            details = floor_details.get(floor, [])
            print(f"\n楼层 {floor} 的 {len(details)} 条记录:")
            for detail in details:
                print(f"  索引 {detail['index']:4d}: UID={detail['uid']:12.0f}, 昵称={detail['nick']}")
    else:
        print("\n✓ 所有楼层值都是唯一的！")

    print("\n" + "=" * 60)


def check_floor_range_and_gaps(file_path):
    """
    检查楼层范围和是否有缺失的楼层

    Args:
        file_path: JSON文件路径
    """
    print("\n" + "=" * 60)
    print("楼层范围和缺失检查")
    print("=" * 60)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        edifice = data.get('data', {}).get('edifice', [])

        if not edifice:
            print("edifice数组为空")
            return

        # 提取所有floor值
        floors = [item.get('floor') for item in edifice if 'floor' in item]

        if not floors:
            print("没有找到floor值")
            return

        # 找出最小和最大的楼层
        min_floor = min(floors)
        max_floor = max(floors)

        print(f"楼层范围: {min_floor} 到 {max_floor}")
        print(f"理论楼层总数: {int(max_floor - min_floor + 1)}")
        print(f"实际楼层总数: {len(floors)}")

        # 检查是否有缺失的楼层
        floor_set = set(floors)
        expected_floors = set(range(int(min_floor), int(max_floor) + 1))

        missing_floors = expected_floors - floor_set

        if missing_floors:
            print(f"\n发现 {len(missing_floors)} 个缺失的楼层:")
            # 将缺失的楼层排序并分组显示
            missing_sorted = sorted(missing_floors)
            print(f"  缺失楼层: {missing_sorted}")
        else:
            print("\n✓ 楼层序列完整，没有缺失")

        # 检查楼层是否连续
        sorted_floors = sorted(floors)
        gaps = []
        for i in range(1, len(sorted_floors)):
            diff = sorted_floors[i] - sorted_floors[i - 1]
            if diff != 1:
                gaps.append((sorted_floors[i - 1], sorted_floors[i], diff))

        if gaps:
            print(f"\n发现 {len(gaps)} 处楼层不连续:")
            for gap in gaps:
                print(f"  在 {gap[0]} 和 {gap[1]} 之间: 间隔 {gap[2]}")
        else:
            print("\n✓ 所有楼层连续排列")

    except Exception as e:
        print(f"检查楼层范围时出错: {str(e)}")

    print("=" * 60)


def main():
    """
    主函数
    """
    # 指定文件路径
    file_path = r"E:\项目\2025\121_12月钻粉活动\jmeter验证送礼\floor_datas.json"

    # 检查重复
    result = check_duplicate_floors_from_file(file_path)

    if result.get('error', False):
        print(f"错误: {result['message']}")
        return

    if not result.get('file_exists', False):
        print(f"错误: 文件不存在 - {file_path}")
        return

    # 打印详细结果
    print_detailed_results(result)

    # 检查楼层范围和缺失
    check_floor_range_and_gaps(file_path)

    # 额外信息
    print("\n" + "=" * 60)
    print("额外统计信息")
    print("=" * 60)

    if not result.get('error', False) and result.get('total_count', 0) > 0:
        print(f"重复率: {result.get('duplicate_count', 0) / result.get('total_count', 1) * 100:.2f}%")

        if result.get('has_duplicates', False):
            # 找出重复次数最多的楼层
            duplicates = result.get('duplicates', {})
            if duplicates:
                max_duplicate_floor = max(duplicates.items(), key=lambda x: x[1])
                print(f"重复次数最多的楼层: {max_duplicate_floor[0]} (出现{max_duplicate_floor[1]}次)")

        # 检查是否有负楼层
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            edifice = data.get('data', {}).get('edifice', [])
            negative_floors = [item.get('floor') for item in edifice if 'floor' in item and item.get('floor') < 0]

            if negative_floors:
                print(f"发现 {len(negative_floors)} 个负楼层: {sorted(negative_floors)}")
            else:
                print("没有负楼层")

        except Exception as e:
            print(f"检查负楼层时出错: {str(e)}")

    print("=" * 60)


if __name__ == "__main__":
    main()