from selenium import webdriver
from bs4 import BeautifulSoup


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
    browser.quit()
    return soup

def get_page_by_code(course_code):
    try:
        target_soup = _get_page_by_helper(course_code, 'Course')
        return target_soup
    except:
        return None

def get_page_by_title(course_title):
    try:
        target_soup = _get_page_by_helper(course_title, 'Title')
        return target_soup
    except:
        return None

def _to_days(days_abv):
    full_days = []
    if 'M' in days_abv:
        full_days.append('Monday')
    if 'T' in days_abv:
        full_days.append('Tuesday')
    if 'W' in days_abv:
        full_days.append('Wednesday')
    if 'R' in days_abv:
        full_days.append('Thursday')
    if 'F' in days_abv:
        full_days.append('Friday')
    return full_days

def _get_data_helper(entry):
    cells = entry.find_all('td')
    # Avaliability
    full_aval = cells[2].get_text().split(" ")
    spots_aval = full_aval[0].split("/")[0]
    spots_aval = int(spots_aval)
    total_aval = full_aval[0].split("/")[1]
    total_aval = int(total_aval)
    # Location
    full_loc = cells[4].get_text()
    full_loc = full_loc.split("/ ")
    days_loc = full_loc[0].strip().split()[0]
    days_loc = _to_days(days_loc)
    full_time = full_loc[0].strip().split()[1]
    if 'M' not in full_time:
        start_time = 'N/A'
        end_time = 'N/A'
    else:
        start_time = full_time.split("-")[0]
        end_time = full_time.split("-")[1]
    room_loc = full_loc[1]
    # Course Code
    full_code = cells[0].get_text().split(" - ")
    course_code = full_code[0]
    course_code = course_code.replace("  ", " ")
    sec_code = full_code[1]
    # Course Title
    course_title = cells[1].get_text().strip()
    # Prof
    full_name = cells[5].get_text().split(", ")
    if len(full_name) >= 2:
        first_name = full_name[1]
        last_name = full_name[0]
        prof_name = first_name + ' ' + last_name
    else:
        prof_name = cells[5].get_text()

    course_info = {
        "course_title": course_title,
        "course_code": course_code,
        "sec_code": sec_code,
        "prof_name": prof_name,
        "spots_aval": spots_aval,
        "total_aval": total_aval,
        "days_loc": days_loc,
        "start_time": start_time,
        "end_time": end_time,
        "room_loc": room_loc
    }

    return course_info

def get_data(soup):
    if soup is None:
        return {"matches": []}

    all_class_info = []

    entries = soup.find("table").find("tbody").find_all("tr")
    for entry in entries:
        if len(entries) <= 1:
            return {"matches": []}
        try:
            res = _get_data_helper(entry)
            all_class_info.append(res)
        except:
            error = {"error": "String Parsing Error"}
            all_class_info.append(error)
                
    return {"matches": all_class_info}