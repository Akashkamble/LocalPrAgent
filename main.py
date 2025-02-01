import asyncio
from reviewer.reviewer import PRReviewer
from logger.logger import get_logger
from settings.config import get_settings

async def review_pr(pr_url: str) -> None:
    """Review a pull request"""
    reviewer = PRReviewer(pr_url)
    await reviewer.review()

def main():
    """Main entry point for the PR reviewer"""
    # parser = argparse.ArgumentParser(description='Review a pull request')
    # parser.add_argument('pr_url', help='URL of the pull request to review')
    # args = parser.parse_args()

    try:
        asyncio.run(review_pr(get_settings().get("config.pr_link")))
    except Exception as e:
        get_logger().error(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()