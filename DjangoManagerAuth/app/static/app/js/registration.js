//     ---------------      Регистрация         -------------------

document.getElementById('closeRegisterBtn').addEventListener('click', function() {
    document.getElementById('registerModal').style.display = 'none';
});

document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Предотвращаем перезагрузку страницы
    const errorDiv = document.getElementById('registerErrors');
    errorDiv.innerText = '';
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    // Валидация паролей
    if (data.password !== data.password_confirm) {
        document.getElementById('registerErrors').innerText = 'Пароли не совпадают';
        return;
    }

    // Отправка на backend
    fetch('/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // ваш способ получить CSRF токен
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json().then(json => ({status: response.status, body: json})))
    .then(({status, body}) => {
        if (status === 200 || status === 201) {
            alert('Регистрация прошла успешно!');
            document.getElementById('registerModal').style.display = 'none';
            form.reset();
        } else {
            errorDiv.innerText = JSON.stringify(body);
        }
    })
    .catch(() => {
        errorDiv.innerText = 'Ошибка при отправке запроса';
    });
});





