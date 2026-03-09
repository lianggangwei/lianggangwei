import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web.scraper import WebScraper, GithubRepoScraper


def example_simple_scrape():
    print("=== 简单网页抓取示例 ===")
    scraper = WebScraper("https://example.com")
    data = scraper.scrape_single_page("https://example.com")
    print(f"标题: {data['title']}")
    print(f"描述: {data['description']}")
    print(f"文本长度: {len(data['text'])}")
    print(f"链接数量: {len(data['links'])}")
    print()


def example_github_scraper():
    print("=== GitHub仓库信息示例 ===")
    scraper = GithubRepoScraper("lianggangwei", "lianggangwei")
    repo_info = scraper.get_repo_info()
    if repo_info:
        print(f"仓库名称: {repo_info.get('name')}")
        print(f"描述: {repo_info.get('description')}")
        print(f"星标数: {repo_info.get('stargazers_count')}")
        print(f"Fork数: {repo_info.get('forks_count')}")
    print()


def example_save_data():
    print("=== 保存数据示例 ===")
    scraper = WebScraper("https://example.com")
    data = scraper.scrape_single_page("https://example.com")
    results = [{
        'url': data['url'],
        'title': data['title'],
        'description': data['description']
    }]
    scraper.save_to_json(results, 'example_data.json')
    scraper.save_to_csv(results, 'example_data.csv')
    print("数据已保存到 example_data.json 和 example_data.csv")
    print()


if __name__ == "__main__":
    try:
        example_simple_scrape()
        example_github_scraper()
        example_save_data()
        print("所有示例运行完成！")
    except Exception as e:
        print(f"示例运行出错: {e}")
