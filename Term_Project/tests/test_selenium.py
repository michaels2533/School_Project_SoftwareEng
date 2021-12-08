import pytest
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep

@pytest.fixture
def student1():
    return {'username':'student', 'firstname':'Student1', 'lastname':'WSU', 'email':'student@wsu.edu', 'password':'1'}

@pytest.fixture
def faculty1():
    return {'username':'faculty', 'firstname':'Faculty1', 'lastname':'WSU', 'email':'faculty@wsu.edu', 'password':'1'}

@pytest.fixture
def browser():
    CHROME_PATH = "C:\\Users\musa\Downloads\chromedriver_win32"
    #CHROME_PATH = "C:\\\\chromedriver_win32"
    print(CHROME_PATH)
    opts = Options()
    opts.headless = False
    driver = webdriver.Chrome(options = opts, executable_path= CHROME_PATH + '\chromedriver.exe')
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_studentRegister(browser, student1):
    
    browser.get("http://localhost:5000/register")

    browser.find_element_by_name("username").send_keys(student1['username'])
    sleep(0.5)
    browser.find_element_by_name("firstname").send_keys(student1['firstname'])
    sleep(0.5)
    browser.find_element_by_name("lastname").send_keys(student1['lastname'])
    sleep(0.5)
    browser.find_element_by_name("email").send_keys(student1['email'])
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(student1['password'])
    sleep(0.5)
    browser.find_element_by_name("password2").send_keys(student1['password'])
    sleep(0.5)
    
    userType = Select(browser.find_element_by_name("userType"))
    userType.select_by_visible_text("Student")
    sleep(0.5)

    browser.find_element_by_name("submit").click()
    sleep(3)
    content = browser.page_source
    assert "Congrats, you are now registered!" in content

def test_studentEditProfile(browser, student1):

    #Login
    browser.get("http://localhost:5000/login")
    browser.find_element_by_name("username").send_keys(student1['username'])
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(student1['password'])
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)

    #Edit profile
    browser.get("http://localhost:5000/student_edit_profile")
    browser.find_element_by_name("major").send_keys("Computer Science")
    sleep(0.5)
    browser.find_element_by_name("GPA").send_keys("3.3")
    sleep(0.5)
    browser.find_element_by_name("gradDate").send_keys("2023")
    sleep(0.5)

    browser.find_element_by_xpath("/html/body/div[2]/form/ul[1]/li[1]/input").click()
    sleep(0.5)

    browser.find_element_by_xpath("/html/body/div[2]/form/ul[2]/li[1]/input").click()
    sleep(0.5)

    browser.find_element_by_xpath("/html/body/div[2]/form/ul[3]/li[4]/input").click()
    sleep(0.5)
    
    browser.find_element_by_name("password").send_keys(student1['password'])
    sleep(0.5)
    browser.find_element_by_name("password2").send_keys(student1['password'])
    sleep(3)

    browser.find_element_by_id("submit").click()
    sleep(3)

    content = browser.page_source
    assert "Your changes have been saved!" in content

def test_facultyRegister(browser, faculty1):

    browser.get("http://localhost:5000/register")

    browser.find_element_by_name("username").send_keys(faculty1['username'])
    sleep(0.5)
    browser.find_element_by_name("firstname").send_keys(faculty1['firstname'])
    sleep(0.5)
    browser.find_element_by_name("lastname").send_keys(faculty1['lastname'])
    sleep(0.5)
    browser.find_element_by_name("email").send_keys(faculty1['email'])
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(faculty1['password'])
    sleep(0.5)
    browser.find_element_by_name("password2").send_keys(faculty1['password'])
    sleep(0.5)
    
    userType = Select(browser.find_element_by_name("userType"))
    userType.select_by_visible_text("Faculty")
    sleep(0.5)

    browser.find_element_by_name("submit").click()
    sleep(3)
    content = browser.page_source
    assert "Congrats, you are now registered!" in content

def test_facultyEditProfile(browser, faculty1):
    #Login
    browser.get("http://localhost:5000/login")
    browser.find_element_by_name("username").send_keys(faculty1['username'])
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(faculty1['password'])
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)

    #Edit profile
    browser.get("http://localhost:5000/faculty_edit_profile")
    browser.find_element_by_name("officehours").send_keys("MW 1-2pm")
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(faculty1['password'])
    sleep(0.5)
    browser.find_element_by_name("password2").send_keys(faculty1['password'])
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)
    content = browser.page_source
    assert "Your changes have been saved!" in content

def test_createPost(browser, faculty1):
    #Login
    browser.get("http://localhost:5000/login")
    browser.find_element_by_name("username").send_keys(faculty1['username'])
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(faculty1['password'])
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)

    #Create Post
    browser.get("http://localhost:5000/createpost")
    browser.find_element_by_name("title").send_keys("Post Test 1")
    sleep(0.5)
    browser.find_element_by_name("description").send_keys("Selenium Test for post 1")
    sleep(0.5)
    browser.find_element_by_name("start").send_keys("01/01/2022")
    sleep(0.5)
    browser.find_element_by_name("end").send_keys("08/31/2022")
    sleep(0.5)

    timeRequired = Select(browser.find_element_by_name("requiredTime"))
    timeRequired.select_by_visible_text("25 Hours")
    sleep(0.5)

    browser.find_element_by_name("qualifications").send_keys("Are able to work.")
    sleep(0.5)

    browser.find_element_by_xpath("/html/body/div[2]/form/div/span/ul/li[1]/input").click()
    sleep(0.5)

    browser.find_element_by_name("submit").click()
    sleep(3)

    content = browser.page_source
    assert "Your Research post has be created!" in content

def test_applyToPostition(browser, student1):

    #Login
    browser.get("http://localhost:5000/login")
    browser.find_element_by_name("username").send_keys(student1['username'])
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(student1['password'])
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)

    #Apply
    
    browser.find_element_by_xpath("/html/body/div[2]/div/div/table/tbody/tr[2]/td[2]/form/input").click()
    sleep(3)

    browser.find_element_by_name("firstName").send_keys("Reference1First")
    sleep(0.5)
    browser.find_element_by_name("lastName").send_keys("Reference1Last")
    sleep(0.5)
    browser.find_element_by_name("email").send_keys("reference1@wsu.edu")
    sleep(0.5)
    browser.find_element_by_name("body").send_keys("I want the job.")
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)


def test_acceptForInterview(broswer, faculty1):
    #Login
    browser.get("http://localhost:5000/login")
    browser.find_element_by_name("username").send_keys(faculty1['username'])
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(faculty1['password'])
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)

    #Change Status
    browser.find_element_by_xpath("/html/body/nav/div/div/ul/li[4]/a").click()
    sleep(1)
    browser.find_element_by_xpath("/html/body/div[2]/table[2]/tbody/tr/td[5]/form/input").click()
    sleep(1)

    status = Select(browser.find_element_by_name("statusfield"))
    status.select_by_visible_text("Hired")
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)

def test_withdrawApplication(browser, student1):
    #Login
    browser.get("http://localhost:5000/login")
    browser.find_element_by_name("username").send_keys(student1['username'])
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(student1['password'])
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)

    #Withdrawal
    browser.find_element_by_xpath("/html/body/div[2]/div/div/input").click()
    sleep(1)

def test_deletePost(browser, faculty1):
    #Login
    browser.get("http://localhost:5000/login")
    browser.find_element_by_name("username").send_keys(faculty1['username'])
    sleep(0.5)
    browser.find_element_by_name("password").send_keys(faculty1['password'])
    sleep(0.5)
    browser.find_element_by_name("submit").click()
    sleep(3)

    #Delete post
    browser.find_element_by_xpath("/html/body/div[2]/div/div/table/tbody/tr[2]/td[2]/a").click()
    sleep(2)

    content = browser.page_source
    assert "Your Research post has been DELETED!" in content

if __name__ == "__main__":
    retcode = pytest.main()