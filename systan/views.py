from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Words, Phrases, Student, WordsFalse, PhrasesFalse
import random

def mkDataSet(type, stage, chapter, mode, student_id):
    start_end_index = {
        'Stage1': [(1, 100), (101, 200), (201, 300), (301, 400), (401, 500), (501, 600),],
        'Stage2': [(601, 700), (701, 800), (801, 900), (901, 1000), (1001, 1100), (1101, 1200),],
        'Stage3': [(1201, 1300), (1301, 1400), (1401, 1500), (1501, 1600), (1601, 1700),],
        'Stage4': [(1701, 1800), (1801, 1900), (1901, 2027),],
        'Stage5': [(2028, 2127), (2128, 2227), (2228, 2327), (2328, 2445),],
    }
    japanese_list, english_list, index_list = [], [], []
    
    try:
        chapter = int(chapter)
        (start_index, end_index) = start_end_index[stage][chapter+1]
    except:
        start_index = start_end_index[stage][0][0]
        end_index = start_end_index[stage][-1][1]
    if mode == 'review':
        if type == 'words':
            object_list = WordsFalse.objects.filter(student_id=student_id, words_id__gte=start_index, words_id__lte=end_index, state=True)
            if len(object_list) >= 1:
                for i in random.sample(range(len(object_list)), len(object_list)):
                    japanese_list.append(object_list[i].words.japanese)
                    english_list.append(object_list[i].words.english)
                    index_list.append(object_list[i].words_id)
        elif type == 'phrases':
            object_list = PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=start_index, phrases_id__lte=end_index, state=True)
            if len(object_list) >= 1:
                for i in random.sample(range(len(object_list)), len(object_list)):
                    japanese_list.append(object_list[i].phrases.japanese)
                    english_list.append(object_list[i].phrases.english)
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
            WordsFalse.objects.update_or_create(student_id=student_id, words_id=id, defaults={'state': True})
        else:
            WordsFalse.objects.update_or_create(student_id=student_id, words_id=id, defaults={'state': False})
    Student.objects.get(id=student_id).save()

def phrases_register_false(all_id, false_id, student_id):
    for id in all_id:
        if id in false_id:
            PhrasesFalse.objects.update_or_create(student_id=student_id, phrases_id=id, defaults={'state': True})
        else:
            PhrasesFalse.objects.update_or_create(student_id=student_id, phrases_id=id, defaults={'state': False})
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
            else:
                error_message = '入力できるのは001から999までの整数値です。'
                return render(request, 'systan/login_prompt.html', {'error_message':error_message})
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