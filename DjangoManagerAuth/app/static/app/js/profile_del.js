// -------------------  МЯГКОЕ Удаление профиля  ------------------------
const deleteProfileBtn = document.getElementById('deleteProfileBtn');

deleteProfileBtn.addEventListener('click', () => {
    if (!confirm('Вы уверены, что хотите удалить свой профиль? Это действие необратимо.')) {
        return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
        alert('Пожалуйста авторизуйтесь');
        return;
    }
    fetch('/api/profile/delete/', {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ is_active: false }) // не обязательно
    })
    .then(async res => {
        if (res.ok) {
            alert(`Профиль удалён (код: ${res.status})`);
            localStorage.removeItem('token');
            window.location.reload();
        } else {
            const data = await res.json();
            alert(`Ошибка ${res.status}: ${data.detail || 'Ошибка удаления профиля'}`);
        }
    })
    .catch(() => alert('Ошибка сети'));

});







    // fetch('/api/profile/delete/', {  
    //     method: 'DELETE',  
    //     headers: {
    //         'Authorization': 'Bearer ' + token,
    //         'Content-Type': 'application/json',                          
    //     },
    //     body: JSON.stringify({ is_active: false })  // Отправка флага отключения
    // })
    // .then(res => {
    //     if (res.ok) {
    //         alert('Профиль удалён');
    //         localStorage.removeItem('token');  // Logout
    //         window.location.reload();          // 
    //     } else {
    //         alert('Ошибка удаления профиля');
    //     }
    // })
    // .catch(() => alert('Ошибка сети'));
