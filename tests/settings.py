from os.path import join

from core.settings import BASE_DIR

__all__ = ["TEST_DIR"]

TEST_DIR = join(BASE_DIR, "tests")
TEST_TEXT_DIR = join(TEST_DIR, "texts")