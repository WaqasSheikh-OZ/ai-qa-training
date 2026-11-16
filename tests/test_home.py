from playwright.sync_api import expect


def test_homepage_opens(home_page):
	expect(home_page.page.locator("body")).to_be_visible()
	
