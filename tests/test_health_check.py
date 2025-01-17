import pytest
import allure
from conftest import api_client
import requests

# Проверяем метод API:ping
@allure.feature('Test Ping')
# Проверяем кейс:Проверка связи или работоспособность API
@allure.story('Test connection')
def test_ping(api_client):
    # Фикстура api_client возвращает нам объект класса api_client
    # И значит нам доступны все методы класса api_client
    with allure.step('Vyzyvaem metod ApiClient:PING'):
        status_code = api_client.ping()
    assert status_code == 201, f'Expected status 201 but got {status_code}'


# Проверяем метод API:ping
@allure.feature('Test Ping')
# Проверяем кейс:Недоступность сервера
@allure.story('Test server unavailability')
def test_ping_server_unavailability(api_client, mocker):
    with allure.step('Otpravlyaem zapros i podmenyaem otvet,vybrasyvaya isklyuchenie:Server unavailability'):
        mocker.patch.object(api_client.session, 'get', side_effect=Exception('Server unavailability'))
        with pytest.raises(Exception, match='Server unavailability'):
            api_client.ping()


# Проверяем метод API:ping
# Данный код позволяет тестировать, как функция ping() обрабатывает ситуацию,
# когда API возвращает статус 405 (Method Not Allowed), не обращаясь к реальному серверу.
@allure.feature('Test Ping')
# Проверяем кейс:Подменяем ответ сервера
@allure.story('Test wrong HTTP method')
def test_ping_wrong_method(api_client, mocker):
    # Создаётся объект mock_response, который является мок-объектом,
    # созданным с помощью библиотеки mocker
    with allure.step('Sozdaem obekt klassa Mock'):
        mock_response = mocker.Mock()
        # Устанавливается атрибут status_code этого мок-объекта на значение 405
        # Это означает, что когда в тесте будет вызван метод, который ожидает получить ответ от API,
        # он получит этот мок-объект с установленным статусом 405 вместо реального ответа от сервера.
    mock_response.status_code = 405
    # Эта строка используется для "замены" метода get объекта api_client на мок-объект.
    # Это значит, что когда в тестах вызывается api_client.get(),
    # вместо реального выполнения этого метода будет возвращено значение mock_response.
    with allure.step('Podmenyaem zapros get, nizhe, i zamenyaem status-kod otveta na 405'):
        mocker.patch.object(api_client.session, 'get', return_value=mock_response)
        # Эта строка создает контекстный менеджер, который ожидает, что внутри
        # блока with будет выброшено исключение AssertionError. Если такое исключение
        # не будет выброшено, тест завершится неудачей.
        # Параметр match используется для проверки сообщения об ошибке. В данном случае проверяется,
        # что сообщение содержит текст 'Expected status code 201 but got 403'.
        # Это полезно для удостоверения, что код действительно вызывает ожидаемую ошибку в случае,
        # если статус-код ответа не соответствует ожидаемому.
        with allure.step('Ozhidaem vybrosa isklyucheniya AssertionError'):
            with pytest.raises(AssertionError, match='Expected status 201 but got 405'):
                # Это вызов метода ping у объекта api_client. Предполагается, что внутри этого метода происходит вызов get,
                # который теперь замокирован и будет возвращать mock_response. Если mock_response имеет статус-код 405,
                # то это приведет к выбросу AssertionError, который мы ожидаем в блоке with.
                api_client.ping()

# Проверяем метод API:ping
# Данный код позволяет тестировать, как функция ping() обрабатывает ситуацию,
# когда API возвращает статус 500, не обращаясь к реальному серверу.
@allure.feature('Test ping')
@allure.story('Test server error')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    with allure.step('Podmenyaem zapros get, nizhe, i zamenyaem status-kod otveta na 500'):
        mocker.patch.object(api_client.session, 'get', return_value=mock_response)
        with allure.step('Ожидаем выброса исключения AssertionError'):
            with pytest.raises(AssertionError, match='Expected status 201 but got 500'):
                api_client.ping()

# Проверяем метод API:ping
# Данный код позволяет тестировать, как функция ping() обрабатывает ситуацию,
# когда API обращается к НЕВЕРНОМУ url.
@allure.feature('Test ping')
@allure.story('Test wrong url')
def test_ping_wrong_url(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    with allure.step('Podmenyaem zapros get, nizhe, i zamenyaem status-kod otveta na 404'):
        mocker.patch.object(api_client.session, 'get', return_value=mock_response)
        with allure.step('Ozhidaem vybrosa isklyucheniya AssertionError'):
            with pytest.raises(AssertionError, match='Expected status 201 but got 404'):
                api_client.ping()

# Проверяем метод API:ping
# Данный код позволяет тестировать, как функция ping() обрабатывает ситуацию,
# когда API возвращает статус 200 вместо 201.
@allure.feature('Test ping')
@allure.story('Test connection with different success code')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    with allure.step('Podmenyaem zapros get, nizhe, i zamenyaem status-kod otveta na 200'):
        mocker.patch.object(api_client.session, 'get', return_value=mock_response)
        with allure.step('Ozhidaem vybrosa isklyucheniya AssertionError'):
            with pytest.raises(AssertionError, match='Expected status 201 but got 200'):
                api_client.ping()

# Проверяем метод API:ping
# Данный код позволяет тестировать, как функция ping() обрабатывает ситуацию,
# когда API возвращает статус 200 вместо 201.
@allure.feature('Test ping')
@allure.story('Test timeout')
def test_ping_timeout(api_client, mocker):
    with allure.step('Podmenyaem zapros get:Ispolzuem Timeout'):
        mocker.patch.object(api_client.session, 'get', side_effect=requests.Timeout)
        with allure.step('Vybrasyvayu isklyuchenie po Timeout'):
            with pytest.raises(requests.Timeout):
                api_client.ping()

# Проверяем метод API:CreateBooking
# Данный код позволяет тестировать, как функция ping() обрабатывает ситуацию,
# когда API возвращает статус 200 вместо 201.
@allure.feature('Test create booking')
@allure.story('Positive:successful create booking')
@pytest.mark.parametrize("client_key", ["client_1", "client_2", "client_3"])
def test_create_booking(api_client, mocker, generate_random_booking_data, client_key):
    # Используем данные из фикстуры для конкретного клиента
    with allure.step('Ispolzuem dannye iz fikstury generate_random_booking_data dlya generacii klienta'):
        payload_booking_data = generate_random_booking_data[client_key]

    # Создание имитации успешного ответа от API
    with allure.step('Sozdanie imitacii uspeshnogo otveta ot API'):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "bookingid": 1,
            "firstname": payload_booking_data["firstname"],
            "lastname": payload_booking_data["lastname"]
        }

    # Имитация метода POST для создания брони
    with allure.step('Proveryaem vyzov metoda post s podgotovlennymi dannymi'):
        mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    # Вызов метода создания бронирования
    with allure.step('Proveryaem vyzov metoda sozdaniya bronirovaniya'):
        response = api_client.create_booking(payload_booking_data)

    # Проверка содержимого ответа
    with allure.step('Proveryaem id bronirovaniya'):
        assert response["bookingid"] == 1
    with allure.step('Proveryaem, chto peredannoe v zaprose firstname sovpadaet s firstname v otvete'):
        assert response["firstname"] == payload_booking_data["firstname"]
    with allure.step('Proveryaem, chto peredannoe v zapross lastname sovpadaet s lastname v otvete'):
        assert response["lastname"] == payload_booking_data["lastname"]