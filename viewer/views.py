from django.shortcuts import render


def hello(request, s0):
    s1 = request.GET['s1']
    return render(
        request, template_name='hello.html',
        context={'adjectives': [s0, s1, 'beautiful', 'wonderful']}
    )
