
window.addEventListener('DOMContentLoaded', () => {
const welcomeNameSpan = document.getElementById('welcomeName');

// Проверяем есть ли токен в localStorage
const token = localStorage.getItem('token');

if (token) {
    // Делаем запрос к API для получения профиля
    fetch('/profile/', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(res => {
    if (!res.ok) throw new Error('Unauthorized');
    return res.json();
    })
    .then(profile => {
    welcomeNameSpan.innerText = ` ${profile.first_name} ${profile.last_name}!`;
    // Здесь можно дополнительно сохранять профиль для дальнейшего использования
    })
    .catch(() => {
    welcomeNameSpan.innerText = ' авторизуйтесь!';
    // Если токен невалиден - можно очистить localStorage
    localStorage.removeItem('token');
    });
} else {
    // Если нет токена, просим авторизоваться
    welcomeNameSpan.innerText = ' авторизуйтесь!';
}
});


function setupModal(openBtnId, modalId, closeBtnId) {
    const openBtn = document.getElementById(openBtnId);
    const modal = document.getElementById(modalId);
    const closeBtn = document.getElementById(closeBtnId);

    openBtn.onclick = () => {
        modal.style.display = 'flex';
    };
    closeBtn.onclick = () => {
        modal.style.display = 'none';
    };
    window.onclick = (e) => {
        if (e.target == modal) {
            modal.style.display = 'none';
        }
    };
}

// Настраиваем модальные окна, навешиваем обрабочики событий
setupModal('openRegisterBtn', 'registerModal', 'closeRegisterBtn'); // регистрация
setupModal('openLoginBtn', 'loginModal', 'closeLoginBtn');          // авторизация
setupModal('openProfileBtn', 'profileModal', 'closeProfileBtn');    // редактирование профиля
setupModal('openRolesBtn', 'rolesModal', 'closeRolesBtn');          // редактирование ролей
//  setupModal('openRolePermissionBtn', 'rolePermissionModal', 'closeRolePermissionBtn');   // редактирование правил





//   --------      Функция для получения CSRF токена из куки (если включён CSRF)  -----------
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//  ---------------     Включение-отключение кнопок   -----------------------
window.addEventListener('DOMContentLoaded', (event) => {
    // Кнопки, которые должны быть активны при загрузке
    const activeButtons = ['openRegisterBtn', 'openLoginBtn'];

    // Все кнопки, которые нужно контролировать
    const allButtons = ['openRegisterBtn', 'openLoginBtn', 'openProfileBtn', 'openRolesBtn', 'logoutBtn', 'deleteProfileBtn'];

    allButtons.forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
            if (activeButtons.includes(id)) {
                btn.disabled = false;
                btn.style.pointerEvents = 'auto';  // сделать кликабельной
                btn.style.opacity = '1';  // нормальная прозрачность
            } else {
                btn.disabled = true;
                btn.style.pointerEvents = 'none'; // не кликабельна
                btn.style.opacity = '0.5'; // полупрозрачная для визуального эффекта отключения
            }
        }
    });
});


           