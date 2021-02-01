from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Question

#質問一覧view
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    # template = loader.get_template('polls/index.html') # DjangoがTemplateを探す時はアプリのtemplatesディレクトリの中から探すからpathに注意
    # return HttpResponse(template.render(context, request))
    #↑ 省略可能 ↑
    return render(request, 'polls/index.html', context) #loader, HttpResponseのimport不要になる

# 質問詳細view
def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
    """
    #↑ 省略可能 ↑
    # getを実行してオブジェクトが存在しない場合にHttp404をレスポンスするときに使う
    # get_list_or_404()もあるが,これはfileterを使用する。リストが空のときに404を返す
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the result of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)