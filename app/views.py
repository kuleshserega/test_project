from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from app.models import Poll, Choice
from django.views import generic

class IndexView(generic.ListView):
	template_name = 'app/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		"""Return the last five published polls."""
		return Poll.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'app/detail.html'

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'app/results.html'


def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# redisplay the poll voting form
		return render(request, 'app/detail.html', {
				'poll' : p,
				'error_message' : "You didn't select a choice",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('app:results', args=(p.id,)))
