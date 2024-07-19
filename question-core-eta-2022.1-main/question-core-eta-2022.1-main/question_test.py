from selenium import webdriver
import unittest
import HtmlTestRunner

from pages import MainPage, QuestionListPage, QuestionAddPage, LoginPage, MessagePage
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class BaseTest(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        self.driver.get("http://core:8000/")

    def tearDown(self):
        self.driver.quit()


class QuestionTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.main_page = MainPage(self.driver)
        self.question_list_page = QuestionListPage(self.driver)
        self.question_add_page = QuestionAddPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.message_page = MessagePage(self.driver)

        self.login_page.login("admin", "123456")

    def test_add_question(self):
        self.main_page.access_menu("Questions")
        self.question_list_page.add_button()
        self.question_add_page.add(text_question="Qual dos advérbios abaixo não existe?",
                                   owner="admin",
                                   choice_one="bastante",
                                   choice_two="quanto",
                                   choice_three="tanto",
                                   choice_four="menas")

        self.assertTrue(self.message_page.success_visible())

    def test_remove_all_questions(self):
        self.main_page.access_menu("Questions")
        self.question_list_page.add_button()
        self.question_add_page.add(text_question="Se uma pessoa age com parcimônia, significa que ela age de forma?",
                                   owner="admin",
                                   choice_one="calma",
                                   choice_two="nervosa",
                                   choice_three="violenta",
                                   choice_four="estúpida")

        self.question_list_page.select_remove_all()

        self.assertTrue(self.message_page.success_visible())


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test_result'))
