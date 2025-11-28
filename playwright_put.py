from playwright.sync_api import sync_playwright, expect
import json

def test_put_user():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        url = "https://jsonplaceholder.typicode.com/users/1"

        payload = {"name": "Jeff Li", "username": "jeffl", "email": "jeff@example.com"}

        # Pass JSON as data string and set content-type
        response = request_context.put(
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
        assert data["id"] == 1
        assert data["name"] == "Jeff Li"

        print("[PASS]Test passed via Playwright!")

if __name__ == "__main__":
    test_put_user()