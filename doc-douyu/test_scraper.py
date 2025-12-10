"""
斗鱼文档抓取器测试脚本
"""
import os
import sys
import json
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import DouyuDocScraper


def test_basic_functionality():
    """测试基本功能"""
    print("测试基本功能...")
    scraper = DouyuDocScraper()
    
    # 测试从URL提取ID
    test_url = "https://doc.douyu.tv/ddse/preview/space/251381?sid=539"
    res_id, sid = scraper.extract_ids_from_url(test_url)
    print(f"从URL提取的ID: res_id={res_id}, sid={sid}")
    
    assert res_id == "251381", f"期望res_id为251381，实际为{res_id}"
    assert sid == "539", f"期望sid为539，实际为{sid}"
    
    print("基本功能测试通过!")
    return True


def test_api_calls():
    """测试API调用（不实际发送请求，只测试方法）"""
    print("\n测试API调用方法...")
    scraper = DouyuDocScraper()
    
    # 测试各个方法是否存在且可调用
    methods = [
        'get_doc_content',
        'get_user_info', 
        'get_attachments',
        'check_collect_status',
        'check_subscribe_status',
        'scrape_page',
        'scrape_from_url',
        'save_content_to_file',
        'get_content_summary'
    ]
    
    for method_name in methods:
        assert hasattr(scraper, method_name), f"方法 {method_name} 不存在"
        method = getattr(scraper, method_name)
        assert callable(method), f"方法 {method_name} 不可调用"
    
    print("API调用方法测试通过!")
    return True


def test_content_processing():
    """测试内容处理功能"""
    print("\n测试内容处理功能...")
    
    # 模拟内容数据
    mock_content_data = {
        'doc_data': {
            'resId': '12345',
            'name': '测试文档',
            'content': '# 标题\n\n这是一篇测试文档。\n\n## 子标题\n\n包含一些内容。',
            'creater': '测试用户',
            'updater': '测试用户',
            'create_time': 1234567890,
            'update_time': 1234567890,
            'views': 10
        },
        'user_info': {'username': 'test'},
        'attachments': [],
        'collect_status': 0,
        'subscribe_status': 0,
        'timestamp': time.time()
    }
    
    scraper = DouyuDocScraper()
    summary = scraper.get_content_summary(mock_content_data)
    
    expected_fields = ['doc_name', 'creator', 'content_length', 'title_count']
    for field in expected_fields:
        assert field in summary, f"摘要中缺少字段: {field}"
    
    assert summary['doc_name'] == '测试文档'
    assert summary['content_length'] == len(mock_content_data['doc_data']['content'])
    assert summary['title_count'] == 2  # # 标题 和 ## 子标题
    
    print("内容处理功能测试通过!")
    return True


def run_all_tests():
    """运行所有测试"""
    print("开始运行斗鱼文档抓取器测试...")
    print("="*50)
    
    tests = [
        test_basic_functionality,
        test_api_calls,
        test_content_processing
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_func.__name__} 通过")
            else:
                print(f"✗ {test_func.__name__} 失败")
        except Exception as e:
            print(f"✗ {test_func.__name__} 异常: {e}")
    
    print("\n" + "="*50)
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("所有测试通过!")
        return True
    else:
        print("部分测试失败!")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)