from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from question.models import Question, Choice
from rest_framework import status
from django.contrib.auth.models import User
from freezegun import freeze_time


class QuestIntegrationTest(APITestCase):
    URL_BASE = 'http://localhost:8000/api/pools/'

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='super_user',
            email='super_user@example.com',
            password='123456'
        )

        self.token = AccessToken.for_user(self.user)

        self.question = Question.objects.create(
            text="Qual foi a primeira linguagem de programação que você aprendendo na faculdade?",
            creation_date="2021-03-01 22:24:57.891964+00:00",
            start_date="2021-03-18 22:24:57.891964+00:00",
            end_date="2021-03-19 22:24:57.891964+00:00",
            owner=self.user
        )

        Choice.objects.create(
            text="Pascal",
            question_id=self.question.id
        )

        Choice.objects.create(
            text="Java",
            question_id=self.question.id
        )
        Choice.objects.create(
            text="C",
            question_id=self.question.id
        )
        Choice.objects.create(
            text="Delphi",
            question_id=self.question.id
        )

    @freeze_time("2021-03-01 22:24:57", tz_offset=-4)
    def test_verificar_se_esta_listando_quest_ainda_nao_iniciada(self):
        data = []
        response = self.client.get(self.URL_BASE + "current/", HTTP_AUTHORIZATION='Bearer {}'.format(self.token))
        self.assertEqual(response.data, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    @freeze_time("2021-03-01 22:24:57", tz_offset=-4)
    def test_verificar_se_esta_listando_quest_criadas_e_nao_iniciadas(self):
        data = []
        response = self.client.get(self.URL_BASE + "closed/", HTTP_AUTHORIZATION='Bearer {}'.format(self.token))
        self.assertEqual(response.data, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_get_para_listar_questoes_sem_token(self):
        response = self.client.get(self.URL_BASE)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_requisicao_get_para_listar_questoes_passando_token(self):
        data = []
        response = self.client.get(self.URL_BASE, HTTP_AUTHORIZATION='Bearer {}'.format(self.token))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNot(response.data, data)

    def test_requisicao_post_para_criar_curso(self):
        data = {
            "text": "Qual a sua linguagem de programação favorita?",
            "creation_date": "2021-03-02 11:07:00",
            "start_date": "2021-03-02 11:07:00",
            "end_date": "2021-03-31 11:07:00",
            "choices": [
                {
                    "text": "Python"
                },
                {
                    "text": "Java Script"
                },
                {
                    "text": "GO"
                },
                {
                    "text": "Java"
                }
            ]
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.URL_BASE, data=data, HTTP_AUTHORIZATION='Bearer {}'.format(self.token),
                                    format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_requisicao_put_para_atualizar_questao(self):
        question = Question.objects.create(
            text="Em qual cidade você gostaria de morar?",
            creation_date="2021-03-01 22:24:57.891964+00:00",
            start_date="2021-03-18 22:24:57.891964+00:00",
            end_date="2021-03-19 22:24:57.891964+00:00",
            owner=self.user
        )

        Choice.objects.create(
            text="Rio de Janeiro",
            question_id=question.id
        )

        Choice.objects.create(
            text="Florianópolis",
            question_id=question.id
        )
        Choice.objects.create(
            text="São Paulo",
            question_id=question.id
        )
        Choice.objects.create(
            text="João Pessoa",
            question_id=question.id
        )

        data = {
            "text": "Qual outro curso você gostaria de fazer?",
            "creation_date": "2021-03-02 11:07:00",
            "start_date": "2021-03-02 11:07:00",
            "end_date": "2021-03-31 11:07:00",
            "choices": [
                {
                    "text": "Python"
                },
                {
                    "text": "Machine Learning"
                },
                {
                    "text": "Docker"
                },
                {
                    "text": "Angular"
                }
            ]
        }
        response = self.client.put(f'{self.URL_BASE}{question.id}/', data=data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(self.token),
                                   format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_deletar_questao(self):
        question = Question.objects.create(
            text="Qual a linguagem de programação mais usada?",
            creation_date="2021-03-01 22:24:57.891964+00:00",
            start_date="2021-03-18 22:24:57.891964+00:00",
            end_date="2021-03-19 22:24:57.891964+00:00",
            owner=self.user
        )

        Choice.objects.create(
            text="JavaScript",
            question_id=question.id
        )

        Choice.objects.create(
            text="Java",
            question_id=question.id
        )
        Choice.objects.create(
            text="Python",
            question_id=question.id
        )
        Choice.objects.create(
            text="Swift",
            question_id=question.id
        )
        Choice.objects.create(
            text="PHP",
            question_id=question.id
        )

        response = self.client.delete(f'{self.URL_BASE}{question.id}/',
                                      HTTP_AUTHORIZATION='Bearer {}'.format(self.token),
                                      format='json')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_or_create_choices_based_on_id(self):
        question = Question.objects.create(
            text="What is your favorite language?",
            owner=self.user
        )

        choice1 = Choice.objects.create(question=question, text="Python")

        data = {
            "text": "What is your favorite programming language?",
            "choices": [
                {"id": choice1.id, "text": "Java"},
                {"text": "C++"},
                {"text": "Ruby"}
            ]
        }

        response = self.client.put(f'{self.URL_BASE}{question.id}/', data=data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(self.token),
                                   format='json')

        self.assertEqual(response.status_code, 200)

        choice1.refresh_from_db()
        self.assertEqual(choice1.text, "Java")

        new_choices = Choice.objects.filter(text__in=["C++", "Ruby"])
        self.assertEqual(new_choices.count(), 2)
