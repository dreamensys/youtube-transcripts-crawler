
from selenium  import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from ResponseResult import ResponseResult

# https://selenium-python.readthedocs.io/waits.html?highlight=wait

class YoutubeScrapper:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def get_video_id(self, url):
        uri_array = "https://www.youtube.com/watch?v=SR5kfWXfxto".split("?")
        id = (uri_array[1])[2:]
        return id

    def get_time(self, str_time):
        time_array = str_time.split(':')
        minutes = int(time_array[0])
        seconds = int(time_array[1])
        return (minutes * 60) + seconds

    def get_element(self, sel ): 
        return self.browser.find_element_by_css_selector(sel)
    
    def get_element_by_css_selector_async(self, sel, delay): 
        return WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))

    def get_child_element_by_class_name_async(self, el, class_name, delay):
        return WebDriverWait(el, delay).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    
    def get_element_by_class_name_async(self, class_name, delay):
        return WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    
    def show_transcripts_panel(self):
        options = self.get_element_by_css_selector_async('ytd-menu-renderer.ytd-video-primary-info-renderer > yt-icon-button:nth-child(2)', 10)
        options.click()
        view_transcripts_element = self.get_element('paper-item.ytd-menu-service-item-renderer')
        view_transcripts_element.click()

    def get_transcript_list_from_video_id(self, video_id):
        url = 'https://www.youtube.com/watch?v='+video_id
        return self.get_transcript_list(url)

    def get_transcript_list(self, url):
        captions = []
        result = ResponseResult(captions)
        self.browser.get(url)
        try:
            self.show_transcripts_panel()
            transcript_element = self.get_element_by_css_selector_async('ytd-engagement-panel-section-list-renderer.style-scope:nth-child(2) > div:nth-child(2)', 1)
            captions_elements = WebDriverWait(transcript_element, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cue-group'))) #transcript_element.find_elements_by_class_name('cue-group')
        except TimeoutException as identifier:
            result.set_failure("Timeout exception")
            return result
        
        if(len(captions_elements) == 0):
            result.set_failure("No captions found")
            return result

        for caption in captions_elements:
            time_lapse = caption.find_element_by_class_name('cue-group-start-offset')
            sentence = caption.find_element_by_class_name('cues')
            seconds_number = self.get_time(time_lapse.text)
            result.data.append({'time': seconds_number, 'text': sentence.text})
        
        result.set_success()
        return result
    
    def close_browser(self ): 
        if (self.browser):
            self.browser.close()
       
