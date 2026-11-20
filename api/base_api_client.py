from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse


class BaseApiClient:
    """Shared HTTP layer for endpoint clients; the request context carries the API base URL."""

    def __init__(self, request_context: APIRequestContext) -> None:
        self._request = request_context

    def _get(self, endpoint: str, params: dict[str, Any] | None = None) -> APIResponse:
        return self._request.get(endpoint, params=params)
