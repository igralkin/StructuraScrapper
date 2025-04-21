import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def log_block_result(url: str, block_name: str, result: dict):
    if url:
        logging.info(
            f"[{url}] {block_name.upper()} — found: {result['found']}, strategy: {result['strategy']}"
        )
