from report.spiders.report_crawler import ReportCrawler

if __name__ == "__main__":
    crawler = ReportCrawler()
    crawler.crawl()
    crawler.export_json()
