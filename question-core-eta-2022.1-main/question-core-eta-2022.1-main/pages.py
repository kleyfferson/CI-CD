from selenium.webdriver.common.by import By


class BasePage:

    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):

    def login(self, user, password):
        self.driver.find_element(By.NAME, "username").send_keys(user)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "action").click()


class MainPage(BasePage):

    def access_menu(self, menu_option):
        self.driver.find_element(By.XPATH, ("//h6[contains(.,'" + menu_option + "')]")).click()


class MessagePage(BasePage):

    def success_visible(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".toast.success-toast").is_displayed()

    def required_visible(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".errornote").is_displayed()


class QuestionListPage(BasePage):

    def add_button(self):
        self.driver.find_element(By.XPATH, "//a[contains(.,'add')]").click()

    def select_remove_all(self):
        self.driver.find_element(By.CSS_SELECTOR, ".text span").click()
        self.driver.find_element(By.CSS_SELECTOR, ".dropdown-trigger").click()
        self.driver.find_element(By.XPATH, "//li[contains(., 'Remover questions selecionados')]").click()
        self.driver.find_element(By.NAME, "index").click()
        self.driver.find_element(By.CSS_SELECTOR, ".red").click()


class QuestionAddPage(BasePage):

    def add(self, text_question, owner, choice_one, choice_two, choice_three, choice_four):
        self.driver.find_element(By.NAME, "text").send_keys(text_question)
        self.driver.find_element(By.CSS_SELECTOR, ".select-dropdown:nth-child(1)").click()
        self.driver.find_element(By.XPATH, "//span[contains(.,'" + owner + "')]").click()
        self.driver.find_element(By.NAME, "choices-0-text").send_keys(choice_one)
        self.driver.find_element(By.NAME, "choices-1-text").send_keys(choice_two)
        self.driver.find_element(By.NAME, "choices-2-text").send_keys(choice_three)
        self.driver.find_element(By.NAME, "choices-3-text").send_keys(choice_four)
        self.driver.find_element(By.CSS_SELECTOR, ".open-actions > button").click()
