const quiz_number = document.querySelector('#quiz_number');
const quiz_length = document.querySelector('#quiz_length');
const question_display = document.querySelector('.question');
const answer_display = document.querySelector('.answer');
const correct_btn = document.querySelector('#correct');
const incorrect_btn = document.querySelector('#incorrect');
const eng = document.querySelector('.english');
const jap = document.querySelector('.japanese');

const el = document.getElementsByClassName("quiz_result");
function getCheckedCount() {
    let total_number = 0;
    let count = 0;
    for (let i = 0; i < el.length; i++) {
        total_number++;
        if (el[i].checked) {
            count++;
        }
    }
    document.querySelector('.correct_number').innerText = total_number - count;
    incorrect_number = document.querySelector('.incorrect_number').innerText = count;
}

let i = 0;
quiz_length.innerText = question_list.length;
question_display.innerHTML = question_list[i];
answer_display.addEventListener('click', (e) => {
    answer_display.innerHTML = answer_list[i];
});

function quiz(CheckedOrNot) {
    i++;
    quiz_number.innerText = i+1;
    question_display.innerHTML = question_list[i];
    answer_display.innerHTML = "解答を表示";
    var li1 = document.createElement('li');
    li1.innerHTML = '<span>'+question_list[i-1]+'</span><input class="quiz_result '+index_list[i-1]+'" type="checkbox" name="false_id" value="'+index_list[i-1]+'"'+CheckedOrNot+'>';
    var li2 = document.createElement('li');
    li2.innerText = answer_list[i-1]
    eng.prepend(li1);
    jap.prepend(li2);
    document.getElementsByClassName(index_list[i-1])[0].addEventListener('click', (e) => {
        getCheckedCount();
    });
    getCheckedCount();
    if(i>=question_list.length){
        document.querySelector('.gamepad').style.display = 'none';
    };
}

correct_btn.addEventListener('click', (e) => {
    quiz('');
})
incorrect_btn.addEventListener('click', (e) => {
    quiz('checked');
})

document.querySelector('.table ul').onclick = () => {
    document.querySelector('.game-end input').classList.toggle('close');
};