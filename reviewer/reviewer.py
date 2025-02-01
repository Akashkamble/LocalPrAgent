from typing import Optional, Dict, Any
from jinja2 import Environment, StrictUndefined

from logger.logger import get_logger
from gitprovider import get_git_provider_from_url
from prhandler.ollama_handler import OllamaAIHandler
from settings.config import get_settings

import re

class PRReviewer:
    def __init__(self, pr_url: str):
        """Initialize PR reviewer with URL and necessary components"""
        self.pr_url = pr_url
        self.git_provider = get_git_provider_from_url(pr_url)
        self.ai_handler = OllamaAIHandler()

    async def review(self):
        """Perform the PR review and return the results"""
        try:
            if not self.git_provider.get_files():
                get_logger().info(f"PR has no files: {self.pr_url}")
                return

            get_logger().info(f'Reviewing PR: {self.pr_url}')
            for filename, file_diff in self.git_provider.get_diff_by_file().items():
                first_line_number = self.extract_first_line_number(file_diff)
                try:
                    diff_metadata = {
                        "language": self.git_provider.get_main_language(),
                        "filename": filename,
                        "diff": file_diff
                    }
                    review_result = await self._get_ai_review(diff_metadata)
                    if not review_result:
                        return
                    review_score = self.extract_score(review_result)
                    get_logger().info(f"Review score: {review_score}")
                    if review_score and review_score < get_settings().get("config.review_score_threshold", 70):
                        get_logger().info(f"Review Response: {review_result}")
                        # Post the review
                        comment = "This file needs to be reviewed manually. AI Review score: " + str(review_score)
                        filename = filename
                        self.git_provider.publish_review_comment(comment, filename, first_line_number)

                except Exception as e:
                    get_logger().error(f"Error during review: {e}")

            get_logger().info("Review completed successfully")

        except Exception as e:
            get_logger().error(f"Error during review: {e}")


    async def _get_ai_review(self, metadata :Dict[str, Any]) -> Optional[str]:
        """Get AI review for the PR"""
        try:
            # Prepare prompts
            environment = Environment(undefined=StrictUndefined)

            system_prompt = environment.from_string(
                get_settings().prompts["pr_review"]["system"]
            ).render()

            user_prompt = environment.from_string(
                get_settings().prompts["pr_review"]["user"]
            ).render(metadata)

            # Get AI completion
            response, _ = await self.ai_handler.chat_completion(
                model=get_settings().get("ollama.model"),
                system=system_prompt,
                user=user_prompt,
                temperature=get_settings().get("ollama.temperature", 0.2)
            )

            return response.strip()

        except Exception as e:
            get_logger().error(f"Error getting AI review: {e}")
            return None

    @staticmethod
    def extract_diff_chunks(diff_text: str) -> list[Dict[str, Any]]:
        """
            Extracts diff chunks from a patch file.
            Returns a list of dictionaries containing the chunk header and lines.
            """
        chunks = []
        current_chunk = []
        chunk_header = None

        for line in diff_text.split("\n"):
            if line.startswith("@@"):
                if current_chunk:
                    chunks.append({"header": chunk_header, "lines": current_chunk})
                    current_chunk = []
                chunk_header = line
            else:
                current_chunk.append(line)

        if current_chunk:
            chunks.append({"header": chunk_header, "lines": current_chunk})

        return chunks

    @staticmethod
    def extract_score(text: str) -> Optional[int]:
        """
        Extracts a numerical score from the DeepSeek review response.
        Returns the extracted score or None if not found.
        """
        match = re.search(r'"?score"?:\s*(\d+)', text)
        return int(match.group(1)) if match else None

    @staticmethod
    def extract_first_line_number(diff_text) -> Optional[int]:
        """
        Extracts the first line number from a Git diff file.
        Returns the first line number as an integer.
        """
        match = re.search(r"@@ -\d+,\d+ \+(\d+)", diff_text)
        return int(match.group(1)) if match else None