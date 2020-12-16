from report.spiders.report_crawler import ReportCrawler
import report.utils as conf

if __name__ == "__main__":
    if conf.base_path_empty:
        crawler = ReportCrawler()
        crawler.crawl()
        crawler.export_json()
    # do report
