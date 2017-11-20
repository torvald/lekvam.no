from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Max

from .models import Note
from .models import List

from .forms import NoteForm

import common.tools.image_tools as image_tools

import datetime
import random

def todo(request):
    lists = _get_lists(request)

    query = request.GET.get('query') or ""

    return render(request, 'todo.html', {'lists': lists,
                                         'query': query})

def _get_list_as_string(request, listid):
    query = request.GET.get('query') or ""

    context = {'user': request.user}
    notes = _get_notes(request.user, listid)

    if query:
        notes = notes.filter(text__icontains=query)
    # recipes = paginate(request, recipes)

    context['list'] = notes
    return render_to_string('list.html', context)

def _get_notes(user, listid):
    return Note.objects.filter(
            Q(owner=user.id) &
            Q(listid=listid) &
            Q(done__isnull=True) &
            Q(deleted__isnull=True)
            ).order_by('weight', 'updated_at')

def ajax_mark_as_done(request, note_id):
    if not request.user.is_authenticated:
        raise PermissionDenied
    note = get_object_or_404(Note, id=note_id)
    _only_allow_owner(request, note)
    note.done = datetime.datetime.now()
    note.save()
    return HttpResponse(_get_list_as_string(request, note.listid))

def ajax_add_note(request):
    """
    Only called by ajax
    """
    if not request.user.is_authenticated():
        raise PermissionDenied
    return HttpResponse(_add_note(request))

def ajax_move_note(request, note_id):
    if not request.user.is_authenticated:
        raise PermissionDenied
    note = get_object_or_404(Note, id=note_id)
    _only_allow_owner(request, note)

    to_listid = _list_name_to_id(request.POST['toListid'])
    from_listid = _list_name_to_id(request.POST['fromListid'])
    to_index = request.POST['toIndex']

    note.listid = to_listid
    note.weight = to_index
    note.save()

    _recalc_weights(request.user, note.id, to_index, from_listid, to_listid)

    return HttpResponse('') # just retun a 200

def _add_note(request):
    form = NoteForm(request.POST or None, request.FILES or None)

    notes = _get_notes(request.user, request.POST['listid'])
    last_weight = notes.aggregate(Max('weight'))['weight__max']
    new_weight = last_weight + 1 if last_weight is not None else 0

    if form.is_valid():
        note = form.save(commit=False)
        note.owner = request.user
        note.weight = new_weight
        if 'image' in request.FILES:
            filename, content = image_tools.resize(request.FILES['image'])
            note.image.save(filename, content)
        note.save()
        return _get_list_as_string(request, note.listid)
    else:
        return form.errors

def _only_allow_owner(request, obj):
    if request.user.id != obj.owner.id:
        raise PermissionDenied

def _get_lists(request):
    lists = {}
    if (request.user.is_authenticated()):
        lists['inbox'] = _get_list_as_string(request, List.INBOX)
        lists['next_actions'] = _get_list_as_string(request, List.NEXT_ACTIONS)
        lists['waiting_for'] = _get_list_as_string(request, List.WAITING_FOR)
        lists['references'] = _get_list_as_string(request, List.REFERENCES)
        lists['projects'] = _get_list_as_string(request, List.PROJECTS)
        lists['someday'] = _get_list_as_string(request, List.SOMEDAY)
    else:
        lists['inbox'] =        _generate_random_note()
        lists['next_actions'] = _generate_random_note()
        lists['waiting_for'] =  _generate_random_note()
        lists['references'] =   _generate_random_note()
        lists['projects'] =     _generate_random_note()
        lists['someday'] =      _generate_random_note()
    return lists

def _generate_random_note():
    from loremipsum import get_sentences
    notes = [
               {'preview': ''.join(get_sentences(random.randint(1, 2))),
               'id': index+1,
               'age': str(random.randint(1, 10)) + "d",
               'formated_due': '2017-12-02' if (random.randint(0,10) > 8) else None,
               'image': {'url': "https://lekvam.no/static/imgs/logo.png"} if (random.randint(0,10) > 8) else None,
               'hashtags': ["tag"] if (random.randint(0,10) > 8) else [],
               'text': "Her kan du endre og fikse ting"}
               for index in range(random.randint(0, 10))
            ]
    return render_to_string('list.html', {'list': notes})

def _list_name_to_id(list_name):
    if list_name == 'inbox':
        return List.INBOX
    if list_name == 'next-actions':
        return List.NEXT_ACTIONS
    if list_name == 'waiting-for':
        return List.WAITING_FOR
    if list_name == 'references':
        return List.REFERENCES
    if list_name == 'projects':
        return List.PROJECTS
    if list_name == 'someday':
        return List.SOMEDAY

def _recalc_weights(user, moved_note_id, to_index, from_listid, to_listid=None):
    def fix_gaps_and_jump_over_newly_moved_note(notes, moved_note_id):
        index = -1
        for note in notes:
            index += 1
            if note.id == moved_note_id:
                continue
            note.weight = index
            note.save()

    if to_listid:
        notes = _get_notes(user, to_listid)
        fix_gaps_and_jump_over_newly_moved_note(notes, moved_note_id)

    notes = _get_notes(user, from_listid)
    fix_gaps_and_jump_over_newly_moved_note(notes, moved_note_id)
