from django.shortcuts import render,redirect
from .models import User

import random 


def index(request):
    if 'rand' not in request.session:
        request.session['rand']=random.randint(1, 100) 
    print(request.session['rand'])
    
    if 'counter' not in request.session:
        request.session['counter']=0
        
    context={
        'result':request.session.get('result',''), #pass the results from result function
        'counter':request.session['counter'], #count number of attempts
        'rand':request.session['rand'],
        'success':request.session.get('success',0), #used with if, if success=1 show submit username form after win
    }
    return render(request,'index.html', context)


#compare with rand and pass a massage
def result(request):
    
    request.session['success']=0
    
    if request.method=='POST':
        request.session['counter']+=1 #increase number of attempts
        guess=int(request.POST['num']) #recieve the guess from user by post form
        
        #correct guess, success=1 so submit username form will appear, win massage will appear
        if guess == request.session['rand']:
            request.session['success']=1
            request.session['result']='win'
            
        #lose when reach 5 attempts and the fifth guess is wrong
        elif 5 == request.session['counter'] and (guess > request.session['rand'] or guess < request.session['rand']):
            request.session['result']='lose'
        
        #greater    
        elif guess > request.session['rand']:
            request.session['result']='Too high!'
            
        #lesser
        elif guess < request.session['rand']:
            request.session['result']='Too low!'  
    return redirect('/')


#clear session
def clear(request):
    try:
        del request.session['rand']
        del request.session['counter']
        del request.session['result']
    except KeyError:
        pass
    return redirect('/')

#execute in win situation, ask the user to submit name then remove form after submitting  
def submit_username(request):
    if request.method=="POST":
        request.session['success']=0
        user1=User.objects.create(username=request.POST.get('username'),score=request.session['counter'])
    return redirect('/')

#shows leaderboard ordered by scores
def leaderboard(request):
    print(User.objects.all().order_by('score'))
    context={
        'users':User.objects.all().order_by('score'),
    }
    return render(request,'leaderboard.html',context)