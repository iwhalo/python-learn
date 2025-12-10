"""
斗鱼文档抓取器使用示例
"""
from scraper import DouyuDocScraper
import os


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 创建抓取器实例
    scraper = DouyuDocScraper()
    
    # 要抓取的页面参数
    res_id = "251381"
    sid = "539"
    
    # 抓取页面内容
    content_data = scraper.scrape_page(res_id, sid)
    
    if content_data:
        print("✓ 成功抓取页面内容")
        
        # 打印文档基本信息
        doc_data = content_data['doc_data']
        print(f"文档名称: {doc_data.get('name', 'N/A')}")
        print(f"创建者: {doc_data.get('creater', 'N/A')}")
        print(f"内容长度: {len(doc_data.get('content', ''))} 字符")
        
        # 保存到文件
        scraper.save_content_to_file(content_data, "output")
        print("✓ 内容已保存到 output/ 目录")
    else:
        print("✗ 抓取失败")


def example_from_url():
    """从URL抓取示例"""
    print("\n=== 从URL抓取示例 ===")
    
    scraper = DouyuDocScraper()
    
    # 目标URL
    url = "https://doc.douyu.tv/ddse/preview/space/251381?sid=539"
    
    # 从URL抓取内容
    content_data = scraper.scrape_from_url(url)
    
    if content_data:
        print("✓ 成功从URL抓取内容")
        
        # 生成摘要
        summary = scraper.get_content_summary(content_data)
        print(f"文档名称: {summary.get('doc_name', 'N/A')}")
        print(f"创建者: {summary.get('creator', 'N/A')}")
        print(f"标题数: {summary.get('title_count', 0)}")
        
        # 保存内容
        scraper.save_content_to_file(content_data, "output", "example")
        print("✓ 内容已保存")
    else:
        print("✗ 从URL抓取失败")


def example_custom_headers():
    """自定义请求头示例"""
    print("\n=== 自定义请求头示例 ===")
    
    # 创建抓取器并自定义基础URL和超时时间
    scraper = DouyuDocScraper(base_url="https://doc.douyu.tv", timeout=60)
    
    # 可以添加额外的请求头
    scraper.session.headers.update({
        'Referer': 'https://doc.douyu.tv/ddse/preview/space/251381?sid=539',
    })
    
    # 抓取内容
    content_data = scraper.scrape_page("251381", "539")
    
    if content_data:
        print("✓ 使用自定义配置抓取成功")
        
        # 显示部分文档内容
        doc_content = content_data['doc_data'].get('content', '')
        preview = doc_content[:100] + "..." if len(doc_content) > 100 else doc_content
        print(f"内容预览: {preview}")
    else:
        print("✗ 自定义配置抓取失败")


def main():
    """主函数"""
    print("斗鱼文档抓取器 - 使用示例")
    print("="*50)
    
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    # 运行示例
    example_basic_usage()
    example_from_url()
    example_custom_headers()
    
    print("\n" + "="*50)
    print("所有示例运行完成!")
    print("输出文件已保存到 output/ 目录")


if __name__ == "__main__":
    main()