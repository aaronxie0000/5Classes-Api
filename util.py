from selenium import webdriver
from bs4 import BeautifulSoup

def pagination():
    pass

def _get_page_by_helper(course, type):
    '''
    type must be: 'Course' or 'Title'
    '''
    url = 'https://portal.claremontmckenna.edu/ics'
    option = webdriver.ChromeOptions()
    option.add_argument("-incognito")
    option.add_argument("--headless")
    browser = webdriver.Chrome('./chromedriver', options=option)

    browser.get(url)

    browser.find_element_by_xpath('//*[@id="pg0_V_lnkToMainView"]').click()
    first_frame = browser.find_element_by_xpath('//*[@id="pg0_V_litFrame"]')
    browser.switch_to.frame(first_frame)
    by_course_field = browser.find_element_by_name(type)
    by_course_field.send_keys(course)
    form_submit = browser.find_element_by_xpath('//*[@id="secondary-container"]/form')
    form_submit.submit()
    browser.switch_to.default_content();
    second_frame = browser.find_element_by_xpath('//*[@id="pg0_V_litFrame"]')
    browser.switch_to.frame(second_frame)
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    return soup


def get_page_by_code(course_code):
    try: 
        target_soup = _get_page_by_helper(course_code, 'Course')
        return target_soup
    except:
        print('Call Error Returning Function')


def get_page_by_title(course_title):
    try: 
        target_soup = _get_page_by_helper(course_title, 'Title')
        return target_soup
    except:
        print('Call Error Returning Function')

def get_data(soup):
    # all_class_info = []

    entries = soup.find("table").find("tbody").find_all("tr")
    for entry in entries:
        cells = entry.find_all('td')
        print(cells[0].get_text())
        print(cells[1].get_text())
        print(cells[2].get_text())
        print(cells[4].get_text())
        print(cells[5].get_text())
        break 


get_data(get_page_by_code('econ120'))

