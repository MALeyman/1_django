// -------------------  Управление ролями    --------------------------
openRolesBtn.addEventListener('click', () => {
    rolesModal.style.display = 'block';

    const token = localStorage.getItem('token');
    console.log('token  token:', token); 

    if (!token) {
    alert('Сначала войдите в систему');
    return;
    }
    
    fetch('/api/users/roles/', {
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }

    })
    .then(res => res.json())
    .then(data => {
    renderRolesTable(data.users, data.roles);
    })
    .catch(() => alert(`Ошибка ${res.status}:Ошибка загрузки данных`));
});

closeRolesBtn.addEventListener('click', () => {
    rolesModal.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target === rolesModal) {
        rolesModal.style.display = 'none';
    }
});


//  заполнение полей ролями
function renderRolesTable(users, roles) {
    const tbody = document.querySelector('#rolesTable tbody');
    tbody.innerHTML = '';

    users.forEach(user => {
        let userRoleIds = [];
        if (user.roles && user.roles.length > 0) {
            userRoleIds = user.roles.map(role => role.id);
        } else {
            // Если ролей нет, назначаем роль User
            const defaultRole = roles.find(role => role.name === 'User');
            if (defaultRole) {
                userRoleIds = [defaultRole.id];
            }
        }

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="border: 1px solid #ccc; padding: 8px;">${user.email}</td>
            <td style="border: 1px solid #ccc; padding: 8px;">
                <select data-user-id="${user.id}">
                    ${roles.map(role => `
                        <option value="${role.id}" ${userRoleIds.includes(role.id) ? 'selected' : ''}>${role.name}</option>`).join('')}
                </select>
            </td>
            <td style="border: 1px solid #ccc; padding: 8px;">
                <button class="saveRoleBtn" data-user-id="${user.id}">Сохранить</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    document.querySelectorAll('.saveRoleBtn').forEach(button => {
        button.addEventListener('click', () => {
            const userId = button.dataset.userId;
            const select = document.querySelector(`select[data-user-id="${userId}"]`);
            const selectedRoleId = select.value;
            saveUserRole(userId, selectedRoleId);
        });
    });
}

//  Отправка изменений на сервер
function saveUserRole(userId, roleId) {
    const token = localStorage.getItem('token');

    fetch(`/api/users/${userId}/role/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({ role_id: roleId })
    })
    .then(res => {
        if (res.ok) {
            alert(`Роль успешно обновлена! (код: ${res.status})`);
        } else {
            // текст ошибки
            res.json().then(data => {
                alert(`Ошибка ${res.status}: ${data.detail || 'Ошибка 1 при обновлении роли'}`);
            }).catch(() => {
                alert(`Ошибка ${res.status}: 'Ошибка 2 при обновлении роли'`);
            });
        }
    })
    .catch(() => {
        alert('Ошибка сети');
    });

}



