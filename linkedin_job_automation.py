#!/usr/bin/env python3
"""
LinkedIn Job Search and Application Automation Script
Automates job searching and application process for Principal/Senior Software Engineer positions
"""

import asyncio
from playwright.async_api import async_playwright, Page
import json
import time
from datetime import datetime, timedelta
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_automation.log'),
        logging.StreamHandler()
    ]
)

class LinkedInJobAutomation:
    def __init__(self):
        self.page = None
        self.context = None
        self.browser = None
        
        # User profile information
        self.user_profile = {
            "name": "Alexander Fedin",
            "email": "jobs4alex@allconnectix.com",
            "phone": "(425)351-1652",
            "location": "San Jose, CA",
            "experience_years": "15+",
            "current_title": "Principal Software Engineer",
            "willing_to_relocate": True,
            "visa_status": "Green Card Holder"
        }
        
        # Job search criteria
        self.search_criteria = {
            "keywords": [
                "Principal Software Engineer",
                "Senior Software Engineer", 
                "Staff Software Engineer",
                "Lead Software Engineer",
                "AI/ML Engineer",
                "Machine Learning Engineer",
                "Distributed Systems Engineer"
            ],
            "location": "San Jose, CA",
            "experience_level": ["Mid-Senior level", "Executive"],
            "job_type": ["Full-time"],
            "posted_time": "Past week",
            "companies_to_prioritize": [
                "Google", "Meta", "Apple", "Amazon", "Microsoft", "Tesla", "NVIDIA",
                "OpenAI", "Anthropic", "Uber", "Lyft", "Airbnb", "Netflix", "Spotify"
            ],
            "exclude_companies": [],
            "required_skills": [
                "AI/ML", "Machine Learning", "Distributed Systems", "Cloud Computing",
                "AWS", "Azure", "GCP", "Angular", "TypeScript", "C++", "C#", ".NET",
                "Python", "Kubernetes", "Docker", "Microservices"
            ]
        }
        
        self.applied_jobs = []
        
    async def setup_browser(self):
        """Initialize browser with persistent session"""
        try:
            self.playwright = await async_playwright().start()
            
            # Use persistent context to maintain login session
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir="/Users/alexanderfedin/Library/CloudStorage/OneDrive-Personal/Resumes/playwrite",
                headless=False,  # Set to True for headless mode
                slow_mo=1000,    # Slow down actions for stability
                viewport={'width': 1920, 'height': 1080},
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            self.page = await self.context.new_page()
            
            # Set user agent to avoid detection
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            logging.info("Browser setup completed successfully")
            
        except Exception as e:
            logging.error(f"Error setting up browser: {str(e)}")
            raise
    
    async def login_to_linkedin(self):
        """Navigate to LinkedIn and handle login if needed"""
        try:
            await self.page.goto('https://www.linkedin.com/login')
            await self.page.wait_for_load_state('networkidle')
            
            # Check if already logged in
            if '/feed' in self.page.url or '/jobs' in self.page.url:
                logging.info("Already logged in to LinkedIn")
                return True
            
            # Manual login required - wait for user to complete
            logging.info("Please complete LinkedIn login manually...")
            logging.info("Once logged in, the script will continue automatically")
            
            # Wait for successful login (redirect to feed or jobs page)
            try:
                await self.page.wait_for_url(lambda url: '/feed' in url or '/jobs' in url, timeout=300000)  # 5 minutes
                logging.info("Login successful!")
                return True
            except:
                logging.error("Login timeout or failed")
                return False
                
        except Exception as e:
            logging.error(f"Error during login process: {str(e)}")
            return False
    
    async def navigate_to_jobs(self):
        """Navigate to LinkedIn Jobs page and set up initial filters"""
        try:
            await self.page.goto('https://www.linkedin.com/jobs/')
            await self.page.wait_for_load_state('networkidle')
            
            logging.info("Navigated to LinkedIn Jobs page")
            
            # Wait for and click on search bar
            search_input = await self.page.wait_for_selector('input[aria-label*="Search by title"]', timeout=10000)
            
            return True
            
        except Exception as e:
            logging.error(f"Error navigating to jobs page: {str(e)}")
            return False
    
    async def setup_search_filters(self, keyword):
        """Set up search filters for job search"""
        try:
            # Enter search keyword
            search_input = await self.page.wait_for_selector('input[aria-label*="Search by title"]')
            await search_input.fill('')  # Clear existing text
            await search_input.type(keyword, delay=100)
            
            # Enter location
            location_input = await self.page.wait_for_selector('input[aria-label*="City"]')
            await location_input.fill('')
            await location_input.type(self.search_criteria["location"], delay=100)
            
            # Click search button
            search_button = await self.page.wait_for_selector('button[aria-label="Search"]')
            await search_button.click()
            
            await self.page.wait_for_load_state('networkidle')
            
            # Apply filters
            await self.apply_advanced_filters()
            
            logging.info(f"Search filters applied for keyword: {keyword}")
            return True
            
        except Exception as e:
            logging.error(f"Error setting up search filters: {str(e)}")
            return False
    
    async def apply_advanced_filters(self):
        """Apply advanced filters like date posted, experience level, etc."""
        try:
            # Click on "All filters" button
            filters_button = await self.page.wait_for_selector('button[aria-label*="filter"]', timeout=5000)
            await filters_button.click()
            
            await asyncio.sleep(2)
            
            # Date posted filter - Past week
            try:
                date_posted_button = await self.page.wait_for_selector('button:has-text("Date posted")', timeout=3000)
                await date_posted_button.click()
                
                past_week_option = await self.page.wait_for_selector('label:has-text("Past week")', timeout=3000)
                await past_week_option.click()
            except:
                logging.warning("Could not set date posted filter")
            
            # Experience level filter
            try:
                experience_button = await self.page.wait_for_selector('button:has-text("Experience level")', timeout=3000)
                await experience_button.click()
                
                for level in self.search_criteria["experience_level"]:
                    level_option = await self.page.wait_for_selector(f'label:has-text("{level}")', timeout=2000)
                    await level_option.click()
            except:
                logging.warning("Could not set experience level filter")
            
            # Job type filter
            try:
                job_type_button = await self.page.wait_for_selector('button:has-text("Job type")', timeout=3000)
                await job_type_button.click()
                
                for job_type in self.search_criteria["job_type"]:
                    type_option = await self.page.wait_for_selector(f'label:has-text("{job_type}")', timeout=2000)
                    await type_option.click()
            except:
                logging.warning("Could not set job type filter")
            
            # Apply filters
            apply_button = await self.page.wait_for_selector('button:has-text("Show results")', timeout=5000)
            await apply_button.click()
            
            await self.page.wait_for_load_state('networkidle')
            
            logging.info("Advanced filters applied successfully")
            
        except Exception as e:
            logging.warning(f"Some filters could not be applied: {str(e)}")
    
    async def get_job_listings(self):
        """Extract job listings from current page"""
        try:
            await self.page.wait_for_selector('.jobs-search-results__list-item', timeout=10000)
            
            job_elements = await self.page.query_selector_all('.jobs-search-results__list-item')
            jobs = []
            
            for element in job_elements:
                try:
                    # Extract job information
                    title_element = await element.query_selector('.job-card-list__title')
                    company_element = await element.query_selector('.job-card-container__company-name')
                    location_element = await element.query_selector('.job-card-container__metadata-item')
                    link_element = await element.query_selector('a.job-card-container__link')
                    
                    if title_element and company_element and link_element:
                        title = await title_element.inner_text()
                        company = await company_element.inner_text()
                        location = await location_element.inner_text() if location_element else "Location not specified"
                        job_url = await link_element.get_attribute('href')
                        
                        # Clean up the data
                        title = title.strip()
                        company = company.strip()
                        location = location.strip()
                        
                        if job_url and not job_url.startswith('http'):
                            job_url = 'https://www.linkedin.com' + job_url
                        
                        job_info = {
                            'title': title,
                            'company': company,
                            'location': location,
                            'url': job_url,
                            'element': element
                        }
                        
                        jobs.append(job_info)
                        
                except Exception as e:
                    logging.warning(f"Error extracting job info from element: {str(e)}")
                    continue
            
            logging.info(f"Found {len(jobs)} job listings on current page")
            return jobs
            
        except Exception as e:
            logging.error(f"Error getting job listings: {str(e)}")
            return []
    
    async def should_apply_to_job(self, job_info):
        """Determine if we should apply to this specific job"""
        try:
            title = job_info['title'].lower()
            company = job_info['company'].lower()
            
            # Check if it's a relevant position
            relevant_keywords = ['principal', 'senior', 'staff', 'lead', 'ai', 'ml', 'machine learning', 
                               'distributed', 'systems', 'software engineer']
            
            has_relevant_keyword = any(keyword in title for keyword in relevant_keywords)
            
            # Check if company is in priority list
            is_priority_company = any(priority_company.lower() in company 
                                    for priority_company in self.search_criteria["companies_to_prioritize"])
            
            # Check if company should be excluded
            is_excluded_company = any(excluded.lower() in company 
                                    for excluded in self.search_criteria["exclude_companies"])
            
            # Basic filtering logic
            should_apply = (has_relevant_keyword and not is_excluded_company)
            
            if is_priority_company:
                logging.info(f"Priority company found: {company}")
                should_apply = True
            
            return should_apply
            
        except Exception as e:
            logging.error(f"Error evaluating job application criteria: {str(e)}")
            return False
    
    async def click_job_and_apply(self, job_info):
        """Click on job and attempt to apply"""
        try:
            # Click on the job to open details
            await job_info['element'].click()
            await asyncio.sleep(3)
            
            # Look for "Easy Apply" button
            easy_apply_button = await self.page.query_selector('button:has-text("Easy Apply")')
            
            if not easy_apply_button:
                # Look for alternative apply button
                easy_apply_button = await self.page.query_selector('.jobs-apply-button')
            
            if easy_apply_button:
                logging.info(f"Attempting to apply to: {job_info['title']} at {job_info['company']}")
                
                await easy_apply_button.click()
                await asyncio.sleep(2)
                
                # Handle the application process
                success = await self.handle_application_process(job_info)
                
                if success:
                    self.applied_jobs.append({
                        'title': job_info['title'],
                        'company': job_info['company'],
                        'location': job_info['location'],
                        'url': job_info['url'],
                        'applied_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'Applied'
                    })
                    
                    logging.info(f"Successfully applied to: {job_info['title']} at {job_info['company']}")
                    await self.update_tracking_file()
                    
                return success
            else:
                logging.info(f"No Easy Apply option for: {job_info['title']} at {job_info['company']}")
                return False
                
        except Exception as e:
            logging.error(f"Error applying to job {job_info['title']}: {str(e)}")
            return False
    
    async def handle_application_process(self, job_info):
        """Handle the multi-step application process"""
        try:
            max_steps = 10
            step = 0
            
            while step < max_steps:
                step += 1
                
                # Check if we're on a form page
                next_button = await self.page.query_selector('button[aria-label="Continue to next step"]')
                submit_button = await self.page.query_selector('button[aria-label="Submit application"]')
                review_button = await self.page.query_selector('button:has-text("Review")')
                
                if submit_button:
                    # Final submission
                    await submit_button.click()
                    await asyncio.sleep(2)
                    
                    # Check for success confirmation
                    success_indicator = await self.page.query_selector('.artdeco-inline-feedback--success')
                    if success_indicator:
                        return True
                    
                elif next_button:
                    # Fill out form fields if present
                    await self.fill_application_form()
                    await next_button.click()
                    await asyncio.sleep(2)
                    
                elif review_button:
                    await review_button.click()
                    await asyncio.sleep(2)
                    
                else:
                    # Look for any other continue/next buttons
                    continue_buttons = await self.page.query_selector_all('button[type="submit"], button:has-text("Next"), button:has-text("Continue")')
                    
                    if continue_buttons:
                        await continue_buttons[0].click()
                        await asyncio.sleep(2)
                    else:
                        break
                
                # Check if application was completed
                if 'application-submitted' in self.page.url or await self.page.query_selector('.application-submitted'):
                    return True
            
            logging.warning(f"Application process took more than {max_steps} steps, might have failed")
            return False
            
        except Exception as e:
            logging.error(f"Error in application process: {str(e)}")
            return False
    
    async def fill_application_form(self):
        """Fill out common application form fields"""
        try:
            # Phone number field
            phone_inputs = await self.page.query_selector_all('input[type="tel"], input[name*="phone"], input[aria-label*="phone"]')
            for phone_input in phone_inputs:
                if await phone_input.get_attribute('value') == '':
                    await phone_input.fill(self.user_profile["phone"])
            
            # Email field
            email_inputs = await self.page.query_selector_all('input[type="email"], input[name*="email"]')
            for email_input in email_inputs:
                if await email_input.get_attribute('value') == '':
                    await email_input.fill(self.user_profile["email"])
            
            # Location/City fields
            location_inputs = await self.page.query_selector_all('input[name*="location"], input[name*="city"], input[aria-label*="location"]')
            for location_input in location_inputs:
                if await location_input.get_attribute('value') == '':
                    await location_input.fill(self.user_profile["location"])
            
            # Handle dropdowns for common questions
            await self.handle_common_dropdown_questions()
            
            # Handle text areas for cover letters or additional info
            await self.handle_text_areas()
            
        except Exception as e:
            logging.warning(f"Error filling application form: {str(e)}")
    
    async def handle_common_dropdown_questions(self):
        """Handle common dropdown questions in applications"""
        try:
            # Work authorization questions
            authorization_selects = await self.page.query_selector_all('select')
            for select in authorization_selects:
                label = await self.get_field_label(select)
                if label and any(keyword in label.lower() for keyword in ['work authorization', 'visa', 'eligible']):
                    # Select appropriate option for Green Card holder
                    options = await select.query_selector_all('option')
                    for option in options:
                        option_text = await option.inner_text()
                        if any(phrase in option_text.lower() for phrase in ['yes', 'authorized', 'permanent resident', 'green card']):
                            await select.select_option(await option.get_attribute('value'))
                            break
            
            # Years of experience
            experience_selects = await self.page.query_selector_all('select')
            for select in experience_selects:
                label = await self.get_field_label(select)
                if label and 'experience' in label.lower():
                    options = await select.query_selector_all('option')
                    for option in options:
                        option_text = await option.inner_text()
                        if any(phrase in option_text for phrase in ['10+', '15+', '10-15', '15-20']):
                            await select.select_option(await option.get_attribute('value'))
                            break
            
        except Exception as e:
            logging.warning(f"Error handling dropdown questions: {str(e)}")
    
    async def get_field_label(self, element):
        """Get the label text for a form field"""
        try:
            # Try to find associated label
            field_id = await element.get_attribute('id')
            if field_id:
                label = await self.page.query_selector(f'label[for="{field_id}"]')
                if label:
                    return await label.inner_text()
            
            # Try to find parent container with label
            parent = await element.query_selector('..')
            if parent:
                label = await parent.query_selector('label')
                if label:
                    return await label.inner_text()
            
            return None
            
        except:
            return None
    
    async def handle_text_areas(self):
        """Handle text areas for cover letters or additional information"""
        try:
            text_areas = await self.page.query_selector_all('textarea')
            
            for text_area in text_areas:
                label = await self.get_field_label(text_area)
                placeholder = await text_area.get_attribute('placeholder')
                
                # Check if it's a cover letter field
                if label or placeholder:
                    field_text = (label or '') + ' ' + (placeholder or '')
                    if any(keyword in field_text.lower() for keyword in ['cover letter', 'why', 'interest', 'motivation']):
                        cover_letter = self.generate_cover_letter()
                        await text_area.fill(cover_letter)
                
        except Exception as e:
            logging.warning(f"Error handling text areas: {str(e)}")
    
    def generate_cover_letter(self):
        """Generate a generic cover letter"""
        return """Dear Hiring Manager,

I am writing to express my strong interest in this position. As a Principal Software Engineer with over 15 years of experience in AI/ML, distributed systems, and cloud architecture, I am excited about the opportunity to contribute to your team.

My background includes extensive experience at leading technology companies including NASA, Boeing, Microsoft, Tesla, and most recently at Waymo/Google. I have deep expertise in:

• AI/ML systems and distributed computing architectures
• Cloud platforms (AWS, Azure, GCP) and microservices
• Full-stack development with Angular, TypeScript, C++, and C#/.NET
• Leading cross-functional teams and delivering scalable solutions

I am authorized to work in the US (Green Card holder) and am available for immediate start. I would welcome the opportunity to discuss how my experience can contribute to your team's success.

Thank you for your consideration.

Best regards,
Alexander Fedin
jobs4alex@allconnectix.com
(425) 351-1652"""
    
    async def update_tracking_file(self):
        """Update the markdown tracking file with applied jobs"""
        try:
            tracking_file = "/Users/alexanderfedin/Library/CloudStorage/OneDrive-Personal/Resumes/applied-for.md"
            
            # Read current content
            with open(tracking_file, 'r') as f:
                content = f.read()
            
            # Add new applications
            new_entries = []
            for job in self.applied_jobs:
                if job['title'] not in content:  # Avoid duplicates
                    entry = f"""
### {job['title']} - {job['company']}
- **Location**: {job['location']}
- **Applied Date**: {job['applied_date']}
- **Status**: {job['status']}
- **URL**: {job['url']}

---
"""
                    new_entries.append(entry)
            
            if new_entries:
                # Append new entries
                with open(tracking_file, 'a') as f:
                    f.write('\n'.join(new_entries))
                
                logging.info(f"Updated tracking file with {len(new_entries)} new applications")
            
        except Exception as e:
            logging.error(f"Error updating tracking file: {str(e)}")
    
    async def run_job_search_automation(self):
        """Main automation workflow"""
        try:
            await self.setup_browser()
            
            if not await self.login_to_linkedin():
                logging.error("Failed to login to LinkedIn")
                return False
            
            if not await self.navigate_to_jobs():
                logging.error("Failed to navigate to jobs page")
                return False
            
            # Search for each keyword
            for keyword in self.search_criteria["keywords"]:
                logging.info(f"Searching for jobs with keyword: {keyword}")
                
                if not await self.setup_search_filters(keyword):
                    continue
                
                # Process multiple pages of results
                pages_processed = 0
                max_pages = 3  # Limit to first 3 pages per keyword
                
                while pages_processed < max_pages:
                    jobs = await self.get_job_listings()
                    
                    if not jobs:
                        break
                    
                    applied_count = 0
                    for job in jobs:
                        if await self.should_apply_to_job(job):
                            if await self.click_job_and_apply(job):
                                applied_count += 1
                                
                                # Rate limiting - wait between applications
                                await asyncio.sleep(10)
                                
                                # Limit applications per session
                                if len(self.applied_jobs) >= 20:
                                    logging.info("Reached daily application limit (20)")
                                    return True
                    
                    logging.info(f"Applied to {applied_count} jobs on page {pages_processed + 1}")
                    
                    # Try to go to next page
                    next_button = await self.page.query_selector('button[aria-label="Next"]')
                    if next_button and await next_button.is_enabled():
                        await next_button.click()
                        await self.page.wait_for_load_state('networkidle')
                        pages_processed += 1
                    else:
                        break
                
                # Wait between different keyword searches
                await asyncio.sleep(5)
            
            logging.info(f"Completed job search automation. Applied to {len(self.applied_jobs)} jobs total.")
            return True
            
        except Exception as e:
            logging.error(f"Error in job search automation: {str(e)}")
            return False
        
        finally:
            if self.context:
                await self.context.close()
            if self.playwright:
                await self.playwright.stop()

# Usage
async def main():
    """Main function to run the automation"""
    automation = LinkedInJobAutomation()
    
    try:
        success = await automation.run_job_search_automation()
        if success:
            print("Job search automation completed successfully!")
            print(f"Applied to {len(automation.applied_jobs)} positions")
        else:
            print("Job search automation encountered errors")
            
    except KeyboardInterrupt:
        print("\nAutomation stopped by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())