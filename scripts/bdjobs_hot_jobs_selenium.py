import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import os

class BDJobsHotJobsScraper:
    def __init__(self):
        self.base_url = "https://bdjobs.com/"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def scrape_hot_jobs(self):
        print("Starting to scrape Hot Jobs section...")
        try:
            self.driver.get(self.base_url)
            print("Page loaded, waiting for content...")
            
            hot_jobs_section = self.wait_for_element(By.CLASS_NAME, "m-text-center")
            print("Found Hot Jobs section!")

            time.sleep(5)

            job_cards = self.driver.find_elements(By.CLASS_NAME, "c-card")
            all_jobs = []

            print(f"Found {len(job_cards)} job cards")
            for card in job_cards:
                try:
                    try:
                        logo = card.find_element(By.CSS_SELECTOR, ".companyLogo img")
                        logo_url = logo.get_attribute('src')
                    except:
                        logo_url = 'N/A'

                    try:
                        company_name_spans = card.find_elements(By.CSS_SELECTOR, "h3 .wr")
                        company_name = ' '.join([span.text for span in company_name_spans])
                    except:
                        company_name = 'N/A'

                    job_links = card.find_elements(By.CSS_SELECTOR, ".companyDetails li a")
                    
                    for job_link in job_links:
                        position_spans = job_link.find_elements(By.CLASS_NAME, "wr")
                        position = ' '.join([span.text for span in position_spans])
                        job_url = job_link.get_attribute('href')
                        
                        job_data = {
                            'company_name': company_name,
                            'company_logo_url': logo_url,
                            'position': position,
                            'job_url': job_url,
                            'scraped_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        all_jobs.append(job_data)
                        print(f"Scraped: {job_data['company_name']} - {job_data['position']}")

                except Exception as e:
                    print(f"Error processing job card: {e}")
                    continue

            return all_jobs

        except Exception as e:
            print(f"Error during scraping: {e}")
            return []
        
        finally:
            self.driver.quit()

    def save_to_csv(self, jobs, filename='bdjobs_hot_jobs.csv'):
        if jobs:
            df = pd.DataFrame(jobs)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\nData saved to {os.path.abspath(filename)}")
            print(f"Total hot jobs scraped: {len(jobs)}")
        else:
            print("No jobs to save")

def main():
    scraper = BDJobsHotJobsScraper()
    
    print("Starting the scraping process...")
    jobs = scraper.scrape_hot_jobs()
    
    scraper.save_to_csv(jobs)

if __name__ == "__main__":
    main()