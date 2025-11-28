from playwright.sync_api import sync_playwright, expect
import json

def test_UI_API():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        request_context = p.request.new_context()

        url = "https://jsonplaceholder.typicode.com/users"

        payload = {"name": "Jeff Li", "username": "jeffl", "email": "jeff@example.com"}

        # Pass JSON as data string and set content-type
        response = request_context.post(
            url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )

        expect(response).to_be_ok()
        print("response: ", response)
        print("Status code:", response.status)
        print("Response JSON:", response.json())
        print("[PASS]POST request successful!")

        data = response.json()
        assert data["id"] == 11
        assert data["name"] == "Jeff Li"

        print("[PASS]Test passed via Playwright!")

        page.goto("https://the-internet.herokuapp.com/login", wait_until="networkidle")
        page.fill("input[name='username']", "tomsmith")
        page.fill("input[name='password']", "SuperSecretPassword!")

        # Click login and wait for navigation
        with page.expect_navigation():
            page.click("button[type='submit']")  # [PASS]Use the correct selector

        # Validate login
        expect(page.locator("div#flash")).to_contain_text("You logged into a secure area!")
        print("[PASS]UI login test passed!")

        browser.close()
        

if __name__ == "__main__":
    test_UI_API()