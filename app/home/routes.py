from flask import render_template,request,url_for,session;
from app.home.forms import HomeForm;
from app.home import bp;
from flask_login import current_user,login_required;
from app import db
from app.models import Words,User;
from app.home import utils;
import random;
from sqlalchemy import func;

@bp.route('/index',methods=['GET','POST'])
@login_required
def searchWord():
    form = HomeForm();
    trailingChars = '.,:; ';
    if form.validate_on_submit():
        word = Words.query.filter_by(word=form.word.data.lower().strip(trailingChars)).first();
        if word is not None:
            if word.is_following(user=current_user):
                print("user follows the word");
                word.users.append(current_user);
            meanings = word.meaning.split("~~");
            return render_template('home/index.html',title='Home',form=form,meanings=meanings);
        else:
            meanings = utils.getWordMeaning(form.word.data.lower().strip(trailingChars));
            new_word = Words(word=form.word.data.lower().strip(trailingChars),meaning=meanings);
            new_word.users.append(current_user);
            db.session.add(new_word);
            db.session.commit();
            return render_template('home/index.html',title='Home',form=form,meanings=meanings.split("~~"));
    queryWord = request.args.get('word');
    if queryWord is not None:
        word = Words.query.filter_by(word=queryWord.strip(trailingChars)).first();
        meanings = word.meaning.split("~~");
        return render_template('home/meanings.html',title='Home',meanings=meanings);
    return render_template('home/index.html',title='Home',form=form);

@bp.route('/admin',methods=['GET'])
@login_required
def admin():
    if current_user.username!='admin':
        return "Cannot Access this page!! Only for admins!!";
    deleteWord = request.args.get('delete');
    if deleteWord is not None:
        word = Words.query.filter_by(word=deleteWord).first();
        if word is not None:
            db.session.delete(word);
            db.session.commit();
    allWords = Words.query.all();
    return render_template('home/admin.html',title='Admin',words=allWords);

@bp.route('/words1',methods=['GET'])
@login_required
def getFollowedWords():
    words = current_user.words;
    return render_template('home/userwords.html',title='Words',words=words);

@bp.route('/words',methods=['GET'])
@login_required
def getFollowedWords1():
    page = request.args.get('page',1,type=int);
    words = current_user.words.paginate(page,10,False);
    next_url = None;
    prev_url = None;
    if words.has_next:
        next_url = '/words?page='+str(words.next_num);
    if words.has_prev:
        prev_url = '/words?page='+str(words.prev_num);
    return render_template('home/userwords.html',title='Words',words=words.items,next_url=next_url,prev_url=prev_url);

@bp.route('/quiz',methods=['GET','POST'])
@login_required
def quiz():
    #numQuestions = app.config['NUM_QUIZ_QUESTIONS'];
    numQuestions = 5;
    trailingChars = '.,:; '
    words = current_user.words;
    dictionary = dict();
    for word in words:
        meaningList = word.meaning.split("~~");
        if len(meaningList) > 1:
            if meaningList[1].strip(trailingChars)!='':
                wordMeaning = meaningList[1];
            elif len(meaningList) > 2:
                wordMeaning = meaningList[2];
            else:
                wordMeaning = "to give example of";
        else:
            wordMeaning = meaningList[0];
        dictionary[word.word] = wordMeaning;
        session['dictionary'] = dictionary;
    if request.method=='POST':
        score = 0;
        questionaire_req = session["questionaire"];
        dictionary_req = session['dictionary'];
        result=dict();
        for key in questionaire_req:
            response = request.form[key];
            print(response);
            if response=="yes":
                if questionaire_req[key]==dictionary_req[key]:
                    result[key]="Correct";
                    score+=1;
                else:
                    result[key] = "Incorrect";
            else:
                if questionaire_req[key]!=dictionary_req[key]:
                    result[key]="Correct";
                    score+=1
                else:
                    result[key]="Incorrect";
            print(len(result));
        return render_template('home/results.html',score=str(score),result=result);
    
    questionaire = dict();
    keywords = list(dictionary.keys());
    print(len(keywords));
    numKeyWords = len(keywords);
    i=0;
    while i<numQuestions:
        index=random.randint(0,1000) % numKeyWords;
        key = keywords[index];
        if random.randint(0,10000)%2 == 0:
            questionaire[key]=dictionary[key];
        else:
            wrongMeaning = None;
            while(wrongMeaning is None):
                wrongMeaningId = (random.randint(1,10000) % int(db.session.query(func.count(Words.id)).scalar()));
                wrongMeaning = Words.query.get(int(wrongMeaningId));
            questionaire[key] = dictionary[wrongMeaning.word];
        if len(questionaire)==numQuestions:
            break;
        session['questionaire'] = questionaire;
    return render_template('home/quiz.html',questionaire=questionaire);
    