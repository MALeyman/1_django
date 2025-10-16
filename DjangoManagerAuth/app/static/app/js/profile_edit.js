//   -------------------------                  Редактирование профиля         ------------------------------

document.getElementById('openProfileBtn').addEventListener('click', function() {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Сначала войдите в систему');
        return;
    }
    console.log(" ТОКЕН: ", token);
    fetch('/profile/', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Ошибка получения профиля');
        return response.json();
    })
    .then(profile => {
        const form = document.getElementById('profileForm');
        console.log(form.querySelector('[name="first_name"]'));

        form.querySelector('[name="first_name"]').value = profile.first_name || '';
        form.querySelector('[name="last_name"]').value = profile.last_name || '';
        form.querySelector('[name="middle_name"]').value = profile.middle_name || '';

        document.getElementById('profileModal').style.display = 'flex';
    })
    .catch(error => {
        alert('Не удалось загрузить профиль: ' + error.message);
    });
});


document.getElementById('profileForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const errorDiv = document.getElementById('profileErrors');
    errorDiv.innerText = '';

    const token = localStorage.getItem('token');
    if (!token) {
        errorDiv.innerText = 'Сначала войдите в систему';
        return;
    }

    const form = e.target;
    const data = {};
    new FormData(form).forEach((value, key) => data[key] = value);

    fetch('/profile/', {
        method: 'PUT',  
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json().then(json => ({status: response.status, body: json})))
    .then(({status, body}) => {
        if (status === 200) {
            alert('Профиль обновлён успешно!');
            document.getElementById('profileModal').style.display = 'none';

            // Получить обновленные данные профиля заново
            fetch('/profile/', {
                headers: {
                    'Authorization': 'Bearer ' + token
                }
            })
            .then(res => res.json())
            .then(profile => {
                document.getElementById('welcomeName').innerText = `${profile.first_name || ''} ${profile.last_name || ''}`.trim();
            });
            
        } else {
            errorDiv.innerText = JSON.stringify(body);
        }
    })
    .catch(() => {
        errorDiv.innerText = 'Ошибка при отправке запроса';
    });
});













