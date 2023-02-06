from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from systan.models import WordsFalse, PhrasesFalse, Student
import json
import datetime

# Create your views here.

start_end_index = {
    'Stage1': [(1, 100), (101, 200), (201, 300), (301, 400), (401, 500), (501, 600),],
    'Stage2': [(601, 700), (701, 800), (801, 900), (901, 1000), (1001, 1100), (1101, 1200),],
    'Stage3': [(1201, 1300), (1301, 1400), (1401, 1500), (1501, 1600), (1601, 1700),],
    'Stage4': [(1701, 1800), (1801, 1900), (1901, 2027),],
    'Stage5': [(2028, 2127), (2128, 2227), (2228, 2327), (2328, 2445),],
}

def get_latest_login(student_id):
    with connection.cursor() as c:
        c.execute(f'SELECT latest_login FROM systan_student WHERE id = {student_id}')
        return (c.fetchall()[0][0] + datetime.timedelta(hours=9)).strftime('%m/%d %H:%M')

def get_missed_data(student_id, start_index, end_index, state, kind):
    with connection.cursor() as c:
        c.execute(f'SELECT systan_{kind}.id, systan_{kind}.japanese, systan_{kind}.english FROM systan_{kind} INNER JOIN systan_{kind}false ON systan_{kind}.id = systan_{kind}false.{kind}_id WHERE systan_{kind}false.student_id = {student_id} AND systan_{kind}false.{kind}_id >= {start_index} AND systan_{kind}false.{kind}_id <= {end_index} AND systan_{kind}false.state = {state} ORDER BY RANDOM()')
        return c.fetchall()

def get_random_data(start_index, end_index, kind):
    with connection.cursor() as c:
        c.execute(f'SELECT * FROM systan_{kind} WHERE id >= {start_index} AND id <= {end_index} ORDER BY RANDOM() LIMIT 20')
        return c.fetchall()

def get_all_data(start_index, end_index, kind):
    with connection.cursor() as c:
        c.execute(f'SELECT * FROM systan_{kind} WHERE id >= {start_index} AND id <= {end_index} ORDER BY RANDOM()')
        return c.fetchall()

def set_test_result(correct_index,incorrect_index, kind, student_id):
    student_id = int(student_id)
    if kind == 'words':
        for id in incorrect_index:
            WordsFalse.objects.update_or_create(student_id=student_id, words_id=int(id), defaults={'state': True})
        for id in correct_index:
            WordsFalse.objects.update_or_create(student_id=student_id, words_id=int(id), defaults={'state': False})
    elif kind == 'phrases':
        for id in incorrect_index:
            PhrasesFalse.objects.update_or_create(student_id=student_id, phrases_id=int(id), defaults={'state': True})
        for id in correct_index:
            PhrasesFalse.objects.update_or_create(student_id=student_id, phrases_id=int(id), defaults={'state': False})
    Student.objects.get(id=student_id).save()


# ここからapi用

def user_info(request):
    kind, student_id = request.GET['kind'], int(request.GET['student_id'])
    progress_by_stage = []

    for stage, index_of_stage in start_end_index.items():
        start_index = index_of_stage[0][0]
        end_index = index_of_stage[-1][1]
        if kind == 'words' and stage == 'Stage5':
            continue
        else:
            correct = len(get_missed_data(student_id, start_index, end_index, 0, kind))
            incorrect = len(get_missed_data(student_id, start_index, end_index, 1, kind))
        done = correct + incorrect
        all_ = end_index - start_index + 1
        yet = all_ - done
        progress_by_stage.append((correct, incorrect, yet))
    return JsonResponse(data={'latest_login': get_latest_login(student_id), 'progress': progress_by_stage})

def missed_data(request):
    kind, stage, chapter, student_id = request.GET['kind'], request.GET['stage'], request.GET['chapter'], int(request.GET['student_id'])
    try:
        chapter = int(chapter)
        (start_index, end_index) = start_end_index[stage][chapter-1]
    except:
        start_index = start_end_index[stage][0][0]
        end_index = start_end_index[stage][-1][1]
    return JsonResponse(data={'data': get_missed_data(student_id, start_index, end_index, 1, kind)}) 

def random_data(request):
    kind, stage, chapter = request.GET['kind'], request.GET['stage'], int(request.GET['chapter'])
    try:
        chapter = int(chapter)
        (start_index, end_index) = start_end_index[stage][chapter-1]
    except:
        start_index = start_end_index[stage][0][0]
        end_index = start_end_index[stage][-1][1]  
    return JsonResponse(data={'data': get_random_data(start_index, end_index, kind)}) 

def all_data(request):
    kind, stage, chapter = request.GET['kind'], request.GET['stage'], int(request.GET['chapter'])
    try:
        chapter = int(chapter)
        (start_index, end_index) = start_end_index[stage][chapter-1]
    except:
        start_index = start_end_index[stage][0][0]
        end_index = start_end_index[stage][-1][1]
    return JsonResponse(data={'data': get_all_data(start_index, end_index, kind)}) 

@csrf_exempt
def result(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        set_test_result(body['correct'], body['incorrect'], body['kind'], body['student_id'])
    return JsonResponse(data={"message": "Hello World"}) 