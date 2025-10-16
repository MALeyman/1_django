//           ---------------             Авторизация       -----------------
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const errorDiv = document.getElementById('loginErrors');
    errorDiv.innerText = '';

    const form = e.target;
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => data[key] = value);

    fetch('/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),

        },
        credentials: 'same-origin', 
        body: JSON.stringify(data)
    })
    .then(response => response.json().then(json => ({status: response.status, body: json})))
    .then(({status, body}) => {
        if (status === 200) {
            alert(`Вход выполнен успешно! (код: ${status})`);
            localStorage.setItem('token', body.token);

            // Запросим профиль для имени и фамилии
            fetch('/profile/', {
                headers: {
                    'Authorization': 'Bearer ' + body.token
                }
            })
            .then(res => res.json())
            .then(profile => {
                // console.log('  profile.first_name:', profile.first_name); 
                if (profile.first_name){
                    document.getElementById('welcomeName').innerText = profile.first_name + ' ' + profile.last_name;
                } else {
                    document.getElementById('welcomeName').innerText =  'авторизуйтесь';
                }

                // Блокируем кнопки регистрации и входа
                const openRegisterBtn = document.getElementById('openRegisterBtn');
                const openLoginBtn = document.getElementById('openLoginBtn');


                if (openRegisterBtn) {
                    openRegisterBtn.disabled = true;
                    openRegisterBtn.style.pointerEvents = 'none';  // запретить клики
                    openRegisterBtn.style.opacity = '0.5';    // визуально показать неактивность
                }
                if (openLoginBtn) {
                    openLoginBtn.disabled = true;
                    openLoginBtn.style.pointerEvents = 'none';
                    openLoginBtn.style.opacity = '0.5'
                }
             
                // разблокируем кнопки
                if (openProfileBtn) {
                    openProfileBtn.disabled = false;
                    openProfileBtn.style.pointerEvents = 'auto';
                    openProfileBtn.style.opacity = '1';
                }

                if (openRolesBtn) {
                    openRolesBtn.disabled = false;
                    openRolesBtn.style.pointerEvents = 'auto';
                    openRolesBtn.style.opacity = '1';
                }                             

                
                if (deleteProfileBtn) {
                    deleteProfileBtn.disabled = false;
                    deleteProfileBtn.style.pointerEvents = 'auto';
                    deleteProfileBtn.style.opacity = '1';
                }                             


                // Показываем кнопку выхода
                document.getElementById('logoutBtn').style.display = 'inline-block';

                if (logoutBtn) {
                    logoutBtn.disabled = false;
                    logoutBtn.style.pointerEvents = 'auto';
                    logoutBtn.style.opacity = '1';
                }                   

                
                // Управление видимостью кнопки управления ролями
                if  (profile.is_superuser || profile.roles.some(role => role.name === 'Moderator') || profile.roles.some(role => role.name === 'Admin')) {
                    //document.getElementById('openRolesBtn').style.display = 'inline-block';

                    if (openRolesBtn) {
                        openRolesBtn.disabled = false;
                        openRolesBtn.style.pointerEvents = 'auto';
                        openRolesBtn.style.opacity = '1';
                    }                             

                } else {
                    //document.getElementById('openRolesBtn').style.display = 'none';
                    if (openRolesBtn) {
                        openRolesBtn.disabled = true;
                        openRolesBtn.style.pointerEvents = 'none';
                        openRolesBtn.style.opacity = '0.5';
                    }                             
                }
                    
                //console.log('КНОПКА  editProfileBtn:', editProfileBtn); 
                // Кнопка редактировать профиль
                //document.getElementById('editProfileBtn').style.display = 'inline-block';
            });
            form.reset();
            document.getElementById('loginModal').style.display = 'none';
        } else {
            alert(`Ошибка ${status}: ${body.detail || 'Ошибка входа'}`);
            errorDiv.innerText = body.error || 'Ошибка входа';
        }
    })
    .catch(() => {
        errorDiv.innerText = 'Ошибка при отправке запроса';
    });
});












