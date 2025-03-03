document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('avatarForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userId = form.dataset.userId;
            const formData = new FormData();
            const fileInput = document.getElementById('avatarInput');
            if (!fileInput.files[0]) {
                alert('請選擇檔案');
                return;
            }
            formData.append('file', fileInput.files[0]);
            try {
                const response = await fetch(`/users/${userId}/avatar`, {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    const data = await response.json();
                    window.location.reload();
                } else {
                    const error = await response.json();
                    alert(error.detail || '上傳失敗');
                }
            } catch (error) {
                alert('上傳發生錯誤');
                console.error('Upload error:', error);
            }
        });
    }
});