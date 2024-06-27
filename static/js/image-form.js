document.getElementById('imagem').addEventListener('change', function (e) {
    const reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('foto-perfil').src = e.target.result;
    }
    reader.readAsDataURL(this.files[0]);
});