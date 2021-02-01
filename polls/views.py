from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Choice, Question

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
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POSTは辞書のようなオブジェクト, keyを指定すると送信したデータにアクセスできる
        # request.POST['choice']だと選択された選択IDを文字列で返す(request.POSTの返り値は文字列)
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist): # choiceがない場合のエラー処理
        # エラー文付き質問フォームを見せる renderでtemplateから取り出してくる
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        '''
        POSTデータを正しく扱えたら常にHttpResponseRedirectを返す
        これによりユーザーが戻るボタンを押した場合にデータが2回投稿されるのを防ぐ
        -> Webの基本: POSTデータが成功したら常にHttpResponseRedirectを返す
        '''
        # HttpResponseRedirectはリダイレクト先のURLを引数にとる
        # reverse()を使用することで、view関数中でのURLのハードコードを防げる
        # 関数には制御したいビューの名前と、そのビューに与えるURLパターンの位置引数を与える
        # reverseを使用すると'/polls/3/results/'が返ってくる(3はqueston.idの値, リダイレクト先のURLはresults)
        # で最終的なページを表示する
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))