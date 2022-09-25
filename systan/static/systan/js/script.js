const active = document.querySelector('.active');
const btn = document.querySelector('header nav');

btn.onclick = () => {
    active.classList.toggle('open');
    btn.classList.toggle('open');
};

const close_btn = document.querySelector('.table ul');

close_btn.onclick = () => {
    document.querySelector('.game-end input').classList.toggle('close');
};