from playwright.sync_api import sync_playwright, expect

def test_delete_user():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        
        # Playwright’s APIRequestContext handles requests for you
        url = "https://jsonplaceholder.typicode.com/users/1"
        response = request_context.delete(url)
       
        # Framework provides structured assertions
        expect(response).to_be_ok()   # Checks status code automatically
        print(response)
        
        assert response.status == 200

        print("[PASS]Test passed via Playwright!")


if __name__ == "__main__":
    test_delete_user()