from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Ely Barros', cpf='05194128347',
                    email='elybarros@gmail.com', phone='86-99900-1477')
        self.resp = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'elybarros@gmail.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['elybarros@gmail.com', 'elybarros@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Ely Barros',
                    '05194128347',
                    '86-99900-1477',
                    'elybarros@gmail.com',]

        for content in contents:
            self.assertIn(content, self.email.body)
