document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("user_answer").focus();

    document.querySelector('#user_answer_form').onsubmit = () => {

        // Инициализировать новый запрос
        const request = new XMLHttpRequest();
        const user_answer = document.querySelector('#user_answer').value;
        request.open('POST', '/check_answer');

        // Функция обратного вызова, когда запрос завершен
        request.onload = () => {

            // Извлечение данных JSON из запроса
            const data = JSON.parse(request.responseText);

            // Обновите result div
            if (data.success) {
                // const contents = `Верно!`
                document.querySelector('#result_title').innerHTML = `Верно!`;
                document.getElementById('result_card_body').style.color = 'green'
            } else {
                document.querySelector('#result_title').innerHTML = 'Неверно';
                document.getElementById('result_card_body').style.color = 'red'
            }
            document.getElementById('result_card').className = "card visible";
            document.getElementById("next_question").focus();
        }

        // Добавить данные для отправки с запросом
        const data = new FormData();
        data.append('user_answer', user_answer);
        data.append('user_id', document.querySelector('.user_id_div').id)

        // Послать запрос
        request.send(data);
        return false;
    };
});