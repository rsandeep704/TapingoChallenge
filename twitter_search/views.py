import urllib

from django.shortcuts import render_to_response, RequestContext
from django.views.generic import View

from .search import search_for_mentions, get_min_id, get_max_id

l = list()


class SearchView(View):
    def get(self, request):
        term = request.GET.get('term', 'tapingo')
        max_id = request.GET.get('max_id', None)
        count = request.GET.get('count', 20)
        prev = request.GET.get('prev', 0)

        if max_id is None and prev == 0:
            request.session['prev_stack'] = list()
            request.session['prev_stack'].append({'term': term})

        prev_stack = request.session['prev_stack']

        if not prev == 0:
            print len(prev_stack)
            if len(prev_stack) > 0:
                prev_stack.pop()
            params = dict()
            if len(prev_stack) > 0:
                params = prev_stack.pop()
            max_id = params.get('max_id', None)

        if len(prev_stack) > 0:
            prev_url_dict = dict(prev_stack[len(prev_stack) - 1])
        else:
            prev_url_dict = dict()
            prev_url_dict['term'] = term
        prev_url_dict['prev'] = 1
        if 'max_id' in prev_url_dict.keys():
            del prev_url_dict['max_id']

        if prev == 0 and max_id is not None:
            prev_stack.append({'term': term, 'max_id': max_id})

        request.session['prev_stack'] = prev_stack

        prev_url = '/?' + urllib.urlencode(prev_url_dict)

        tweets = search_for_mentions(term, count=count, max_id=max_id)
        next_url = '/?' + urllib.urlencode({'term': term, 'max_id': get_min_id(tweets)})

        context = dict()
        context['next_url'] = next_url
        context['prev_url'] = prev_url
        context['tweets'] = tweets

        return render_to_response('index.html', context=context, context_instance=RequestContext(request))
