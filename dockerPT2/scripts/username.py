
from playwright.sync_api import Playwright, sync_playwright
from playwright._impl._errors import TargetClosedError
import logging, argparse

logger = logging.getLogger(__name__)

def run(playwright: Playwright, company_name: str, headless, page: int) -> None:
    try:
        browser = playwright.chromium.launch(headless=headless, slow_mo=200)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/122.0.6261.58 Safari/605.1.15')

        page1 = context.new_page()
        page1.goto(f"https://www.startpage.com/search?q=site:linkedin.com/in OR site:linkedin.com/pub -site:linkedin.com/pub/dir at {company_name}")
        # Fill in the search field with the LinkedIn search query for the company.

        print(f"Username enum for: {company_name}\n")
        i=0
        # Repeat the actions for 4 pages (including the first one)
        for _ in range(int(page)):  
            page1.wait_for_selector('.result h2')  # Wait for the results to load
            titles = page1.query_selector_all('.result h2')   #### THE ELEMENTS CAN CHANGE SO IF SCRIPT DOESNT WORK, CHECK! ####

            for title_element in titles:
                if title_element:
                    title = title_element.text_content()
                    i+=1
                    print(f'{i}. Title: {title}')
                else:
                    print("No title found")

            # Check if there is a 'Next' button or link and click it to go to the next page
            next_button = page1.get_by_role("link", name="Next")   #### THE ELEMENTS CAN CHANGE SO IF SCRIPT DOESNT WORK, CHECK! ####
            if next_button:
                next_button.click()
                # Wait for the next page to load
                page1.wait_for_load_state('networkidle')
            else:
                print('No more pages or reached the last page.')
                break

        browser.close()
    
    # Error handling
    except KeyboardInterrupt:
        print("\nScript execution was interrupted by the user.")

    except TimeoutError:
        print(" Operation timed out. The page or element might not have loaded properly.")

    except TargetClosedError as e:
        print("---------------------------")
        print("Attempted to operate on a closed page, context, or browser.")
        browser.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a LinkedIn search for employees of a given company.')
    parser.add_argument('-d', '--domain', required=True, help='Company name to search for is (required!). If there is a space, use (" "), for example: -c "Triple P"')
    parser.add_argument('-p', '--page', required=True, help='Company name to search for is (required!). If there is a space, use (" "), for example: -c "Triple P"')
    parser.add_argument('-hl', '--headless', action='store_true', help='Run browser in headless mode (default: True')
    args = parser.parse_args()
    
    with sync_playwright() as playwright:
        run(playwright, args.domain, headless=args.headless, page=args.page)