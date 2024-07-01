const users = [
    { username: 'maroquio', title: 'Professor Responsável 1', link: 'https://github.com/maroquio', profileImageId: 'profileImage1', githubLinkId: 'githubLink1' },
    { username: 'MirielleRosa', title: 'Aluna 1', link: 'https://github.com/MirielleRosa', profileImageId: 'profileImage2', githubLinkId: 'githubLink2' },
    { username: 'meloMilena', title: 'Aluna 2', link: 'https://github.com/meloMilena', profileImageId: 'profileImage3', githubLinkId: 'githubLink3' }
];

users.forEach(user => {
    const apiUrl = `https://api.github.com/users/${user.username}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const profileImage = document.getElementById(user.profileImageId);
            const githubLink = document.getElementById(user.githubLinkId);

            if (data.avatar_url) {
                profileImage.innerHTML = `<img src="${data.avatar_url}" class="rounded-circle mb-3" width="100" height="100" alt="Profile Image">`;
            }

            if (data.login) {
                githubLink.href = data.html_url;
                githubLink.textContent = data.login;
            }
        })
        .catch(error => console.error(`Error fetching GitHub user data for ${user.username}:`, error));
});