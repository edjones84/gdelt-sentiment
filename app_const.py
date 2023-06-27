from typing import Final

COUNTRY: Final[str] = "UK"
BASE_URL: Final[str] = "https://api.gdeltproject.org/api/v2/doc/doc?"
RECORDS: Final[int] = 10
TIME: Final[str] = "1d"
DESTINATION_LANG: Final[str] = "en"
REQUEST_HEADERS: Final[dict[str, str]] = {'User-agent': 'gdelt bot'}
ALT_ISO691_COUNTRY_CODES: Final[dict[str, str]] = {'chinese': 'zh-CN', 'hebrew': 'iw'}