from playwright.sync_api import sync_playwright, expect

def test_get_user():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        
        # Playwright’s APIRequestContext handles requests for you
        url = "https://jsonplaceholder.typicode.com/users/1"
        response = request_context.get(url)

        print("response JSON: ", response.json()['id'])
        print("response JSON: ", response.json()['name'])
        print("response JSON: ", response.json()['username'])
        print("response JSON: ", response.json()['email'])
        
        # Framework provides structured assertions
        expect(response).to_be_ok()   # Checks status code automatically
        
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Leanne Graham"

        print("[PASS]Test passed via Playwright!")


if __name__ == "__main__":
    test_get_user()