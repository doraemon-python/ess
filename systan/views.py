from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Words, Phrases, Student, WordsFalse, PhrasesFalse
import random

def game_set(type, stage, mode, *student_id):
    japanese_list = []
    english_list = []
    index_list = []
    if type == 'words':
        object_list = Words.objects.all()
    elif type == 'phrases':
        object_list = Phrases.objects.all()
    if stage == 'Stage1':
        object_list = object_list[:600]
    elif stage == 'Stage2':
        object_list = object_list[600:1200]
    elif stage == 'Stage3':
        object_list = object_list[1200:1700]
    elif stage == 'Stage4':
        object_list = object_list[1700:2027]
    elif stage == 'Stage5':
        object_list = object_list[2027:]
    if mode == 'random':
        for i in  random.sample(range(len(object_list)), 20):
            japanese_list.append(object_list[i].japanese)
            english_list.append(object_list[i].english)
            index_list.append(i+1)
    elif mode == 'all':
        for i in range(len(object_list)):
            japanese_list.append(object_list[i].japanese)
            english_list.append(object_list[i].english)
            index_list.append(i+1)
    elif mode == 'review':
        student_id = student_id[0]
        if type == 'words':
            if stage == 'Stage1':
                if WordsFalse.objects.filter(student_id=student_id, words_id__lte=600).exists():
                    object_list = WordsFalse.objects.filter(student_id=student_id, words_id__lte=600)
                else:
                    object_list = False
            elif stage == 'Stage2':
                if WordsFalse.objects.filter(student_id=student_id, words_id__gte=601, words_id__lte=1200).exists():
                    object_list = WordsFalse.objects.filter(student_id=student_id, words_id__gte=601, words_id__lte=1200)
                else:
                    object_list = False
            elif stage == 'Stage3':
                if WordsFalse.objects.filter(student_id=student_id, words_id__gte=1201,  words_id__lte=1700).exists():
                    object_list = WordsFalse.objects.filter(student_id=student_id, words_id__gte=1201,  words_id__lte=1700)
                else:
                    object_list = False
            elif stage == 'Stage4':
                if WordsFalse.objects.filter(student_id=student_id, words_id__gte=1701).exists():
                    object_list = WordsFalse.objects.filter(student_id=student_id, words_id__gte=1701)
                else:
                    object_list = False
            if object_list:
                for i in object_list:
                    japanese_list.append(Words.objects.get(id=i.words_id).japanese)
                    english_list.append(Words.objects.get(id=i.words_id).english)
                    index_list.append(i.words_id)
        elif type == 'phrases':
            if stage == 'Stage1':
                if PhrasesFalse.objects.filter(student_id=student_id, phrases_id__lte=600).exists():
                    object_list = PhrasesFalse.objects.filter(student_id=student_id, phrases_id__lte=600)
                else:
                    object_list = False
            elif stage == 'Stage2':
                if PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=601, phrases_id__lte=1200).exists():
                    object_list = PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=601, phrases_id__lte=1200)
                else:
                    object_list = False
            elif stage == 'Stage3':
                if PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=1201,  phrases_id__lte=1700).exists():
                    object_list = PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=1201,  phrases_id__lte=1700)
                else:
                    object_list = False
            elif stage == 'Stage4':
                if PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=1701, phrases_id__lte=2027).exists():
                    object_list = PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=1701, phrases_id__lte=2027)
                else:
                    object_list = False
            elif stage == 'Stage5':
                if PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=2028).exists():
                    object_list = PhrasesFalse.objects.filter(student_id=student_id, phrases_id__gte=2028)
                else:
                    object_list = False
            if object_list:
                for i in object_list:
                    japanese_list.append(Phrases.objects.get(id=i.phrases_id).japanese)
                    english_list.append(Phrases.objects.get(id=i.phrases_id).english)
                    index_list.append(i.words_id)
            
    return japanese_list, english_list, index_list

def words_register_false(all_id, false_id, student_id):
    for id in all_id:
        if id in false_id:
            if WordsFalse.objects.filter(student_id=student_id, words_id=id).exists():
                pass
            else:
                WordsFalse.objects.create(student_id=student_id, words_id=id)
        else:
            if WordsFalse.objects.filter(student_id=student_id, words_id=id).exists():
                WordsFalse.objects.filter(student_id=student_id, words_id=id).delete()
            else:
                pass
    Student.objects.get(id=student_id).save()

def phrases_register_false(all_id, false_id, student_id):
    for id in all_id:
        if id in false_id:
            if PhrasesFalse.objects.filter(student_id=student_id, words_id=id).exists():
                pass
            else:
                PhrasesFalse.objects.create(student_id=student_id, words_id=id)
        else:
            if PhrasesFalse.objects.filter(student_id=student_id, words_id=id).exists():
                PhrasesFalse.objects.filter(student_id=student_id, words_id=id).delete()
            else:
                pass
    Student.objects.get(id=student_id).save()

# Create your views here.
def login_prompt(request):
    return render(request, 'systan/login_prompt.html')

def words(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        try:
            student_id = int(student_id)
            if student_id <=0 or student_id >=1000:
                return render(request, 'systan/words.html', {"error_message":True})
            return redirect(f'{student_id}/')
        except:
            return render(request, 'systan/words.html', {"error_message":True})
    return render(request, 'systan/words.html')

def phrases(request):
    if request.method == 'POST':
        student_id=request.POST['student_id']
        try:
            student_id = int(student_id)
            return redirect(f'{student_id}/')
        except:
            return render(request, 'systan/phrases.html', {"error_message":True})
    return render(request, 'systan/phrases.html')

def words_individual(request, student_id):
    latest_login = Student.objects.get(id=student_id).latest_login
    return render(request, 'systan/words_individual.html', {'student_id': student_id, 'latest_login':latest_login})

def phrases_individual(request, student_id):
    latest_login = Student.objects.get(id=student_id).latest_login
    return render(request, 'systan/phrases_individual.html', {'student_id': student_id, 'latest_login':latest_login})

def tests(request, type, stage, mode):
    japanese_list, english_list, index_list = game_set(type, stage, mode)
    context = {'japanese_list':japanese_list, 'english_list':english_list, 'index_list':index_list, 'type':type}
    return render(request, 'systan/tests.html', context)

def tests_individual(request, type, stage, mode, student_id):
    japanese_list, english_list, index_list = game_set(type, stage, mode, student_id)
    context = {'japanese_list':japanese_list, 'english_list':english_list, 'index_list':index_list, 'student_id':student_id, 'type':type}
    return render(request, 'systan/tests_individual.html', context)

def show(request, type, stage, mode):
    japanese_list, english_list, index_list = game_set(type, stage, mode)
    context = {'japanese_list':japanese_list, 'english_list':english_list, 'index_list':index_list}
    return render(request, 'systan/show.html', context)

def show_individual(request, type, stage, mode, student_id):
    japanese_list, english_list, index_list = game_set(type, stage, mode, student_id)
    context = {'japanese_list':japanese_list, 'english_list':english_list, 'index_list':index_list, 'student_id':student_id, 'type':type}
    return render(request, 'systan/show_individual.html', context)

def game_data_post(request):
    try:
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
    except:
        if request.POST['type'] == 'words':
            return redirect(f'/systan/words/')
        elif request.POST['type'] == 'phrases':
            return redirect(f'/systan/phrases/')

def others(request):
    return render(request, 'systan/others.html')