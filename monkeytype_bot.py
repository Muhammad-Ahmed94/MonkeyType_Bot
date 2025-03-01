from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import random


class MonkeyTypeBot:
    def __init__(self, wpm_speed=200):
        """
        Initialize the MonkeyType automation bot for Microsoft Edge
        
        Args:
            wpm_speed (int): Target words per minute speed (adjust for desired ranking)
        """
        self.wpm_speed = wpm_speed
        # Set up Edge WebDriver
        service = Service(EdgeChromiumDriverManager().install()) # Change depend on borwser type
        self.driver = webdriver.Edge(service=service)
        self.words = []
        
    def open_monkeytype(self):
        """Open the MonkeyType website and handle any initial popups/cookies"""
        self.driver.get("https://monkeytype.com")
        # Wait for page to load
        time.sleep(2)
        
        # Handle cookie consent if it appears
        try:
            cookie_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "cookie-accept"))
            )
            cookie_button.click()
        except:
            # No cookie popup or different ID
            pass
            
    # Word scraping
    def scrape_words(self):
        """Scrape the words that need to be typed from the active test"""
        try:
            # Wait for the words to be visible
            word_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".word"))
            )
            
            # Extract all words that are visible
            self.words = []
            for word_element in word_elements:
                word = ""
                letter_elements = word_element.find_elements(By.CSS_SELECTOR, "letter")
                for letter in letter_elements:
                    word += letter.text
                if not word:  # If we couldn't get letter by letter, get the whole word
                    word = word_element.text
                if word:
                    self.words.append(word)
                    
            print(f"Scraped {len(self.words)} words")
            return self.words
            
        except Exception as e:
            print(f"Error scraping words: {e}")
            return []
            
    # Actual typing
    def type_with_human_like_speed(self):
        """Type the scraped words with a human-like pattern but very fast"""
        if not self.words:
            print("No words to type!")
            return
            
        # Calculate timing based on WPM
        # Average word length is about 5 characters
        chars_per_minute = self.wpm_speed * 5
        base_delay = 60 / chars_per_minute  # seconds per character
        
        # Create action chains for typing
        actions = ActionChains(self.driver)
        
        # Click on the typing area to focus it
        try:
            typing_area = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "typingTest"))
            )
            typing_area.click()
        except:
            # If we can't find the specific element, click in the middle of the screen
            actions.move_by_offset(0, 0).click().perform()
        
        # Type each word with small random variations in timing
        for word in self.words:
            for char in word:
                # Small random variation to seem more human-like
                delay = base_delay * random.uniform(0.8, 1.2)
                actions.send_keys(char)
                actions.pause(delay)
                
            # Add space after each word
            actions.send_keys(Keys.SPACE)
            actions.pause(base_delay)
            
        # Perform all the typing actions
        actions.perform()
        
    def complete_typing_test(self):
        """Run a complete typing test session"""
        self.open_monkeytype()
        
        # Wait for user to manually select test settings (time, language, etc.)
        input("Set up your test settings (time, mode, etc.) then press Enter to continue...")
        
        # Wait a moment before starting to scrape and type
        time.sleep(2)
        
        # Scrape words and start typing
        self.scrape_words()
        self.type_with_human_like_speed()
        
        # Wait for the test to complete and results to show
        print("Test complete! Check your results.")
        
    def close(self):
        """Close the browser when done"""
        self.driver.quit()


if __name__ == "__main__":
    # Create the bot with a very high WPM (adjust as needed)
    bot = MonkeyTypeBot(wpm_speed=200)
    
    try:
        bot.complete_typing_test()
        
        # Keep the browser open to see results
        input("Press Enter to close the browser...")
    finally:
        bot.close()