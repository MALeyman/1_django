//   -------------------    Выход       ---------------------------
document.getElementById('logoutBtn').addEventListener('click', function() {
    localStorage.removeItem('token');
    document.getElementById('welcomeName').innerText = 'авторизуйтесь!';

    const openRegisterBtn = document.getElementById('openRegisterBtn');
    const openLoginBtn = document.getElementById('openLoginBtn');

    // разблокируем кнопки
    if (openRegisterBtn) {
        openRegisterBtn.disabled = false;
        openRegisterBtn.style.pointerEvents = 'auto';  
        openRegisterBtn.style.opacity = '1';   
    }
    if (openLoginBtn) {
        openLoginBtn.disabled = false;
        openLoginBtn.style.pointerEvents = 'auto';
        openLoginBtn.style.opacity = '1'
    }

    const openProfileBtn = document.getElementById('openProfileBtn');
    const openRolesBtn = document.getElementById('openRolesBtn');
    // блокируем кнопки
    if (openProfileBtn) {
        openProfileBtn.disabled = true;
        openProfileBtn.style.pointerEvents = 'none';
        openProfileBtn.style.opacity = '0.5';
    }

    if (openRolesBtn) {
        openRolesBtn.disabled = true;
        openRolesBtn.style.pointerEvents = 'none';
        openRolesBtn.style.opacity = '0.5';
    }                

    if (deleteProfileBtn) {
        deleteProfileBtn.disabled = true;
        deleteProfileBtn.style.pointerEvents = 'none';
        deleteProfileBtn.style.opacity = '0.5';
    }                

    this.style.display = 'none';  // скрыть кнопку Выйти

});
