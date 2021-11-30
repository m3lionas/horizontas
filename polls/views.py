from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View

from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin

from .forms import UploadFileForm
from .services import handle_uploaded_file

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return published questions."""
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def upload_file(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            tests_passed = handle_uploaded_file(request.FILES['file'], question.testcase_set.all())
            if tests_passed:
                return redirect(reverse('polls:passed'))
            else:
                return redirect(reverse('polls:failed'))
        # else:
        #     msg = 'Errors: %s' % form.errors.as_text()
        #     return HttpResponse(msg, status=400)
    else:
        form = UploadFileForm()
    return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "Nepasirinktas failas",
    })
    # return HttpResponseRedirect(request, 'polls/detail.html', {'form': form})


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return redirect('polls:success')
#     else:
#         form = UploadFileForm()
#     return render(request, 'polls/upload.html', {'form': form})


def passed_tests(request):
    return render(request, 'polls/passed_tests.html')


def failed_tests(request):
    return render(request, 'polls/failed_tests.html')
