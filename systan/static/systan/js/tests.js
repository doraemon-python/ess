
const question_display = document.querySelector('.question');
const answer_display = document.querySelector('.answer');
const correct_btn = document.querySelector('#correct');
const incorrect_btn = document.querySelector('#incorrect');
const eng = document.querySelector('.english');
const jap = document.querySelector('.japanese');

let i = 0;
question_display.innerHTML = question_list[i];
answer_display.addEventListener('click', (e) => {
    answer_display.innerHTML = answer_list[i];
});
correct_btn.addEventListener('click', (e) => {
    i++
    question_display.innerHTML = question_list[i];
    answer_display.innerHTML = "解答を表示";
    var li1 = document.createElement('li')
    li1.innerHTML = '<span>'+question_list[i-1]+'</span><input type="checkbox" name="false_id" value="'+index_list[i-1]+'">'
    var li2 = document.createElement('li');
    li2.innerText = answer_list[i-1]
    eng.prepend(li1);
    jap.prepend(li2);
    if(i>=question_list.length){
        document.querySelector('.gamepad').style.display = 'none';
    };
});
incorrect_btn.addEventListener('click', (e) => {
    i++
    question_display.innerHTML = question_list[i];
    answer_display.innerHTML = "解答を表示";
    var li1 = document.createElement('li');
    li1.innerHTML = '<span>'+question_list[i-1]+'</span><input type="checkbox" name="false_id" value="'+index_list[i-1]+'" checked>'
    var li2 = document.createElement('li');
    li2.innerText = answer_list[i-1]
    eng.prepend(li1);
    jap.prepend(li2);
    if(i>=question_list.length){
        document.querySelector('.gamepad').style.display = 'none';
    };
});

const close_btn = document.querySelector('.table ul');

close_btn.onclick = () => {
    document.querySelector('.game-end input').classList.toggle('close');
};