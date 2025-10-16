
//    --------------------------       Редактирование правил      ----------------------
const openRolePermissionBtn = document.getElementById('openRolePermissionBtn');
const rolePermissionModal = document.getElementById('rolePermissionModal');
const closeRolePermissionBtn = document.getElementById('closeRolePermissionBtn');

openRolePermissionBtn.addEventListener('click', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Сначала войдите в систему');
        return;
    }

    fetch('/api/role-permissions/', {
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
    })
    .then(res => {
        if (res.status === 401) {
            alert(`Ошибка ${res.status}: Вы не авторизованы`);
            throw new Error('Unauthorized');
        }
        if (!res.ok) {
            alert(`Ошибка ${res.status}: Ошибка при загрузке правил`);
            throw new Error('Error fetching');
        }
        return res.json();
    })
    .then(data => {
        const tbody = document.querySelector('#rolePermissionTable tbody');
        tbody.innerHTML = ''; // очистка

        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="border: 1px solid #ccc; padding: 5px;">${item.id}</td>
                <td style="border: 1px solid #ccc; padding: 5px;">${item.role_name}</td>
                <td style="border: 1px solid #ccc; padding: 5px;">${item.permission_codename}</td>
                <td style="border: 1px solid #ccc; padding: 5px;">
                    <button class="edit-btn" data-id="${item.id}">Редактировать</button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        // Открываем модалку только при успешной загрузке
        rolePermissionModal.style.display = 'block';
    })
    .catch(error => {
        console.error(error);
        
    });
});


closeRolePermissionBtn.addEventListener('click', () => {
rolePermissionModal.style.display = 'none';
});

window.addEventListener('click', (event) => {
if (event.target === rolePermissionModal) {
    rolePermissionModal.style.display = 'none';
}
});


