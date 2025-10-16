// Просмотр документов (фиктивные данные)
document.getElementById('openDocumentsBtn').addEventListener('click', function() {
    const token = localStorage.getItem('token');
    console.log("ТОКЕН", token)
    if (!token) {
        alert("Сначала войдите в систему");
        return;
    }

    fetch('/api/check-permission/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => 
        response.json().then(body => ({status: response.status, body}))
    )
    .then(({status, body}) => {
        if (!body.has_permission) {
            alert(`Ошибка ${status}: ${body.detail || 'Доступ запрещён 1'}`);
            return;
        }
  
        const modal = document.getElementById('documentsModal');
        const content = document.getElementById('documentsContent'); 
        modal.style.display = 'block';
        content.innerHTML = 'Загрузка...';

        fetch('/mock/documents/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })  
            .then(response => response.json())
            .then(data => {
                if (data.documents && data.documents.length > 0) {
                    let html = '<ul>';
                    data.documents.forEach(doc => {
                        html += `<li><b>${doc.title}</b>: ${doc.content}</li>`;
                    });
                    html += '</ul>';
                    content.innerHTML = html;
                } else {
                    content.innerHTML = 'Документы не найдены';
                }
            })
            .catch(() => {
                content.innerHTML = 'Ошибка загрузки документов';
            });
    })
    .catch(() => alert("Ошибка проверки прав"));
});


document.getElementById('closeDocumentsBtn').addEventListener('click', function() {
    document.getElementById('documentsModal').style.display = 'none';
});




