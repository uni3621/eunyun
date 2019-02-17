from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Candidate, Poll, Choice
from django.db.models import Sum
import datetime

# Create your views here.
def index(request):
    candidates = Candidate.objects.all()  # 해당 테이블의 모든 row값을 불러온다.(DB에서)
    context = {'candidates': candidates}  # 그 값을 dictionary값으로 contex에 저장하여
    return render(request, 'elections/index.html', context)  # html에게 넘겨준다.

    # html안쓸 떄
    # str = ''
    # for candidate in candidates :
    #    str += "<p>{} 기호{}번({})<br>".format(candidate.name, candidate.party_number, candidate.area) #br넣는 이유 : html로 보여주기 때문에
    #    str += candidate.introduction+"</p>"  #p는 단락 바꿔주는 용도
    # return HttpResponse(str)


def areas(request, area):
    today = datetime.datetime.now() #현재 시간이 투표의 start date보다 크고 end date보다 작아야 됨.
    try :
        poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte= today)
        # 그 지역구의 투표정보를 받아온다. startdate는 today보다크고 endate는 today보다 작은것을 가져와라
        candidates = Candidate.objects.filter(area=area)  # 앞부분의 area는 candidate의 area고,
        #  뒷 부분은 매개변수의 area
        # candidate에서의 area값중에 매개변수의 area와 같은 값만 받아와라.
    except:
        poll = None
        candidates = None
    context = {'candidates': candidates, 'area': area, 'poll':poll}
    return render(request, 'elections/area.html', context)  # context가 area.html로 전달됨. 이후 html을 수정하면 됨.

def polls(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    selection = request.POST.get('choice', False)

    try:
        choice = Choice.objects.get(poll_id=poll.id, candidate_id=selection)
        choice.votes += 1
        choice.save()
    except:
        choice = Choice(poll_id=poll.id, candidate_id=selection, votes=1)
        choice.save()

    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    #후보자 이름
    candidates = Candidate.objects.filter(area=area)

    #기간
    polls = Poll.objects.filter(area=area)
    poll_results = [] #여러 투표가 있으니까
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date

        total_votes = Choice.objects.filter(poll_id=poll.id).aggregate(Sum('votes'))#dict 출력
        result['total_votes'] = total_votes['votes__sum']

        rates = [] #지지율
        for candidate in candidates:
            try:
                choice = Choice.objects.get(poll_id=poll.id, candidate_id=candidate.id)
                rates.append(round(choice.votes*100/result['total_votes'],1))
            except:
                rates.append(0)
        result['rates'] = rates
        poll_results.append(result)

    context = {'candidates': candidates, 'area': area, 'poll_results':poll_results}
    return render(request, 'elections/result.html', context) #이렇게 하면 result.html파일과 연결되어 이 화면 보여줌.
