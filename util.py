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

    # Pagination not needed as is iframe page source gives all
    # all_soups = [soup]
    # all_pages = browser.find_elements_by_xpath('//*[@id="menu"]/div[1]/li[*]')
    # for page in range(0, (len(all_pages) - 3)):
    #     # all_pages[-1].find_element_by_tag_name('a').click()
    #     browser.find_element_by_link_text('»').click()
    #     page_source_new = browser.page_source
    #     soup_new = BeautifulSoup(page_source_new, 'lxml')
    #     print(soup_new.prettify)
    #     # all_soups.append(soup_new)
    # return all_soups


def get_page_by_code(course_code):
    try:
        target_soup = _get_page_by_helper(course_code, 'Course')
        # return target_soup
    except:
        print('Call Error Returning Function')


def get_page_by_title(course_title):
    try:
        target_soup = _get_page_by_helper(course_title, 'Title')
        return target_soup
    except:
        print('Call Error Returning Function')


def get_data(soup):
    all_class_info = []

    entries = soup.find("table").find("tbody").find_all("tr")
    for entry in entries:
        cells = entry.find_all('td')
        if len(cells) < 4:
            if len(entries) < 1:
                # Call no result function
                continue #! to be deleted
            else:
                continue
        # Avaliability
        full_aval = cells[2].get_text().split(" ")
        spots_aval = full_aval[0].split("/")[0]
        total_aval = full_aval[0].split("/")[1]
        # Location
        full_loc = cells[4].get_text()
        full_loc = full_loc.split("/ ")
        # if '\xa0' in full_loc[0]:     
        #     days_loc = full_loc[0].split("\xa0   ")[0]
        #     full_time = full_loc[0].split("\xa0   ")[1].strip()
        # else:
        #     print( full_loc[0].strip().split())
        #     days_loc = full_loc[0].strip().split()[0]
        #     full_time = full_loc[0].strip().split()[1]
        days_loc = full_loc[0].strip().split()[0]
        full_time = full_loc[0].strip().split()[1]
        start_time = full_time.split("-")[0]
        end_time = full_time.split("-")[1]
        room_loc = full_loc[1]
        # Course Code
        full_code = cells[0].get_text().split(" - ")
        course_code = full_code[0]
        course_code = course_code.replace("  ", " ")
        sec_code = full_code[1]
        # Course Title
        course_title = cells[1].get_text()
        # Prof
        full_name = cells[5].get_text().split(", ")
        if len(full_name) >= 2:
            first_name = full_name[1]
            last_name = full_name[0]
            prof_name = first_name + ' ' + last_name
        else:
            prof_name = cells[5].get_text()

        course_info = {
            'course_title': course_title,
            'course_code': course_code,
            'sec_code': sec_code,
            'prof_name': prof_name,
            'spots_aval': spots_aval,
            'total_aval': total_aval,
            'days_loc': days_loc,
            'start_time': start_time,
            'end_time': end_time,
            'room_loc': room_loc
        }
        print(course_info)
        all_class_info.append(course_code)



get_data(get_page_by_title('bio'))
