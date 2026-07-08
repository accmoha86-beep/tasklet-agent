"""Example: Web Search and Scraping"""

import os
import sys
from dotenv import load_dotenv

load_dotenv(".env.infrastructure")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.web_tools import WebSearchTool, WebScrapeTool
from integration.logger_handler import LoggerHandler


def main():
    """Demonstrate web tools"""

    print("🌐 Web Tools Demo")
    print("=" * 60)

    # Initialize tools
    search_tool = WebSearchTool()
    scrape_tool = WebScrapeTool()
    logger_handler = LoggerHandler()

    # Web search
    print(f"\n🔍 Web Search Example:")
    print("-" * 60)
    search_result = search_tool.execute("AI agents architecture", num_results=5)
    print(f"Query: AI agents architecture")
    print(f"Status: {search_result['status']}")
    print(f"Results: {search_result['results']}")

    # Web scrape
    print(f"\n👀 Web Scraping Example:")
    print("-" * 60)
    scrape_result = scrape_tool.execute(
        "https://github.com/accmoha86-beep/tasklet-agent",
        selector=".Box-title"
    )
    print(f"URL: https://github.com/accmoha86-beep/tasklet-agent")
    print(f"Status: {scrape_result['status']}")
    if scrape_result['status'] == 'success':
        print(f"Content length: {len(scrape_result['content'])} chars")
        print(f"Content preview: {scrape_result['content'][:200]}...")

    # Log results
    print(f"\n📋 Logging Web Activities:")
    print("-" * 60)
    log_result = logger_handler.log_execution("web_demo", {
        "search": search_result,
        "scrape": scrape_result,
    })
    print(f"Logged to: {log_result['file']}")

    print(f"\n✅ Demo Complete!")


if __name__ == "__main__":
    main()
