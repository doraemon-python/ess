const active = document.querySelector('.active');
const btn = document.querySelector('header nav');

btn.onclick = () => {
    active.classList.toggle('open');
    btn.classList.toggle('open');
};