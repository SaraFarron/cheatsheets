example:
```py
class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
```
+ `setUpTestData()` вызывается каждый раз перед запуском теста на уровне настройки всего класса. Вы должны использовать данный метод для создания объектов, которые не будут модифицироваться/изменяться в каком-либо из тестовых методов.
+ `setUp()` вызывается перед каждой тестовой функцией для настройки объектов, которые могут изменяться во время тестов (каждая функция тестирования будет получать "свежую" версию данных объектов).

Run tests:
`python3 manage.py test`

Best practices

+ If it can break, it should be tested. This includes models, views, forms, templates, validators, and so forth.
+ Each test should generally only test one function.
+ Keep it simple. You do not want to have to write tests on top of other tests.
+ Run tests whenever code is PULLed or PUSHed from the repo and in the staging environment before PUSHing to production.
+ When upgrading to a newer version of Django:
  + upgrade locally,
  + run your test suite,
  + fix bugs,
  + PUSH to the repo and staging, and then
  + test again in staging before shipping the code.


