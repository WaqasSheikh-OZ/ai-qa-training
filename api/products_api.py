from playwright.sync_api import APIResponse

from api.base_api_client import BaseApiClient


class ProductsApi(BaseApiClient):
    _PRODUCTS_ENDPOINT = "/products"

    def get_products(self, page: int | None = None) -> APIResponse:
        params = {"page": page} if page is not None else None
        return self._get(self._PRODUCTS_ENDPOINT, params=params)
