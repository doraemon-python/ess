from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Words, Phrases, Student, WordsFalse, PhrasesFalse
import random

def mkDataSet(type, stage, chapter, mode, student_id):
    start_index = 0
    end_index = 0
    japanese_list = []
    english_list = []
    index_list = []
    try:
        chapter = int(chapter)
        if stage =='Stage1':
            start_index = 100*chapter - 99
            end_index = 100*chapter
        elif stage == 'Stage2':
            start_index = 100*chapter + 501
            end_index = 100*chapter + 600
        elif stage == 'Stage3':
            start_index = 100*chapter + 1101
            end_index = 100*chapter + 1200
        elif stage == 'Stage4':
            if chapter <= 2:
                start_index = 100*chapter + 1601
                end_index = 100*chapter + 1700
            else:
                start_index = 1901
                end_index = 2027
        elif stage == 'Stage5':
            if chapter <= 3:
                start_index = 100*chapter + 1928
                end_index = 100*chapter + 2107
            else:
                start_index = 2408
                end_index = 2445
    except:
        if stage == 'Stage1':
            start_index = 1
            end_index = 600
        elif stage == 'Stage2':
            start_index = 601
            end_index = 1200
        elif stage == 'Stage3':
            start_index = 1201
            end_index = 1700
        elif stage == 'Stage4':
            start_index = 1701
            end_index = 2027
        elif stage == 'Stage5':
            start_index = 2028
            end_index = 2445
    if mode == 'review':
        if type == 'words':
            object_list = WordsFalse.objects.filter(student_id=student_id, words_id__gte=start_index, words_id__lte=end_index)
            if len(object_list) >= 1:
                for i in random.sample(range(len(object_list)), len(object_list)):
                    japanese_list.append(Words.objects.get(id=object_list[i].words_id).japanese)
                    english_list.append(Words.objects.get(id=object_list[i].words_id).english)
                    index_list.append(object_list[i].words_id)
        elif type == 'phrases':
            object_list = PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=start_index, phrases_id__lte=end_index)
            if len(object_list) >= 1:
                for i in random.sample(range(len(object_list)), len(object_list)):
                    japanese_list.append(Phrases.objects.get(id=object_list[i].phrases_id).japanese)
                    english_list.append(Phrases.objects.get(id=object_list[i].phrases_id).english)
                    index_list.append(object_list[i].phrases_id)
    elif mode == 'random':
        if type == 'words':
            object_list = Words.objects.filter(id__gte=start_index, id__lte=end_index)
        elif type == 'phrases':
            object_list = Phrases.objects.filter(id__gte=start_index, id__lte=end_index)
        for i in  random.sample(range(len(object_list)), 20):
            japanese_list.append(object_list[i].japanese)
            english_list.append(object_list[i].english)
            index_list.append(object_list[i].id)
    elif mode == 'all':
        if type == 'words':
            object_list = Words.objects.filter(id__gte=start_index, id__lte=end_index)
        elif type == 'phrases':
            object_list = Phrases.objects.filter(id__gte=start_index, id__lte=end_index)
        for i in random.sample(range(len(object_list)), len(object_list)):
            japanese_list.append(object_list[i].japanese)
            english_list.append(object_list[i].english)
            index_list.append(object_list[i].id)
    return japanese_list, english_list, index_list

def words_register_false(all_id, false_id, student_id):
    for id in all_id:
        if id in false_id:
            WordsFalse.objects.update_or_create(student_id=student_id, words_id=id)
        else:
            if WordsFalse.objects.filter(student_id=student_id, words_id=id).exists():
                WordsFalse.objects.filter(student_id=student_id, words_id=id).delete()
    Student.objects.get(id=student_id).save()

def phrases_register_false(all_id, false_id, student_id):
    for id in all_id:
        if id in false_id:
            PhrasesFalse.objects.update_or_create(student_id=student_id, phrases_id=id)
        else:
            if PhrasesFalse.objects.filter(student_id=student_id, phrases_id=id).exists():
                PhrasesFalse.objects.filter(student_id=student_id, phrases_id=id).delete()
            else:
                pass
    Student.objects.get(id=student_id).save()

# Create your views here.
def login_prompt(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        try:
            print(student_id)
            student_id = int(student_id)
            if 1 <= student_id <= 999:
                return redirect('systan:home', 'words', student_id)
        except:
            error_message = '入力できるのは001から999までの整数値です。'
            return render(request, 'systan/login_prompt.html', {'error_message':error_message})
    else:
        return render(request, 'systan/login_prompt.html')

def home(request, type, student_id):
    latest_login = Student.objects.get(id=student_id).latest_login
    context = {'type':type, 'student_id':student_id, 'latest_login':latest_login}
    return render(request, 'systan/home.html', context)

def chapter_select(request, type, category, stage, mode, student_id):
    context = {'type':type, 'category':category, 'stage':stage, 'mode':mode, 'student_id':student_id}
    return render(request, 'systan/chapter_select.html', context)

def tests(request, type, category, stage, chapter, mode, student_id):
    japanese_list, english_list, index_list = mkDataSet(type, stage, chapter, mode, student_id)
    context = {
        'japanese_list':japanese_list, 
        'english_list':english_list, 
        'index_list':index_list, 
        'type':type, 
        'category':category, 
        'student_id':student_id
    }
    if category == 'tests':
        return render(request, 'systan/tests.html', context)
    elif category == 'show':
        return render(request, 'systan/show.html', context)

def game_data_post(request):
    student_id = int(request.POST['student_id'])
    all_id = [int(i) for i in request.POST['all_id'][1:-1].split(',')]
    false_id = request.POST.getlist('false_id', [])
    if false_id:
        false_id = [int(i) for i in false_id]
    if request.POST['type'] == 'words':
        words_register_false(all_id, false_id, student_id)
        return redirect(f'/systan/words/{student_id}')
    elif request.POST['type'] == 'phrases':
        phrases_register_false(all_id, false_id, student_id)
        return redirect(f'/systan/phrases/{student_id}')

def others(request, type, student_id):
    context = {'type':type, 'student_id':student_id}
    return render(request, 'systan/others.html', context)