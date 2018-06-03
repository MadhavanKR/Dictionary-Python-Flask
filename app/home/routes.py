from flask import render_template,request,url_for,session;
from app.home.forms import HomeForm;
from app.home import bp;
from flask_login import current_user,login_required;
from app import db,current_app
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
            current_app.logger.info(word.word+" is available in database");
            if word.is_following(user=current_user)==False:
                current_app.logger.info(current_user.username+" does not follow word-"+word.word+"-- adding to follow list");
                word.users.append(current_user);
                db.session.commit();
            meanings = word.meaning.split("~~");
            return render_template('home/index.html',title='Home',form=form,meanings=meanings);
        else:
            current_app.logger.info(form.word.data.lower()+" is not available in database, querying from merriam webster");
            meanings = utils.getWordMeaning(form.word.data.lower().strip(trailingChars));
            if meanings is None:
                return render_template('home/index.html',title='Home',form=form,error="No Meanings found");
            current_app.logger.info("adding "+form.word.data.lower()+" to database and to "+current_user.username+" following list");
            new_word = Words(word=form.word.data.lower().strip(trailingChars),meaning=meanings);
            new_word.users.append(current_user);
            db.session.add(new_word);
            db.session.commit();
            return render_template('home/index.html',title='Home',form=form,meanings=meanings.split("~~"));
    
    queryWord = request.args.get('word');
    if queryWord is not None:
        current_app.logger.info("got query for "+queryWord);
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
    numQuestions = current_app.config['QUIZ_NUM_QUESTIONS'] or 5;
    #numQuestions = 5;
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
    current_app.logger.info("adding dictionary to session "+ str(dictionary));
    current_app.logger.info(current_user.username+" -- dictionary length : "+str(len(dictionary)));
    if len(dictionary) < numQuestions:
        numQuestions = len(dictionary);
        
    if request.method=='POST':
        score = 0;
        questionaire_req = session["questionaire"];
        dictionary_req = session['dictionary'];
        current_app.logger.info("retreived questionaire from session "+str(questionaire_req));
        current_app.logger.info("retreived dictionary from session "+str(dictionary_req));
        if session.get('questionaire') is not None:
            session.pop('questionaire');
        if session.get('dictionary') is not None:
            session.pop('dictionary');
        current_app.logger.info("popping questionaire and dictionary from session ");
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
        return render_template('home/results.html',score=str(score),result=result);
    
    questionaire = dict();
    keywords = list(dictionary.keys());
    current_app.logger.info(keywords);
    numKeyWords = len(keywords);
    i=0;
    while i<numQuestions:
        index=random.randint(0,1000) % numKeyWords;
        key = keywords[index];
        if key in questionaire.keys():
            continue;
        if random.randint(1,10000)%2 == 0:
            questionaire[key]=dictionary[key];
        else:
            wrongMeaning = None;
            while(wrongMeaning is None):
                current_app.logger.info(db.session.query(func.count(Words.id)).scalar());
                wrongMeaningId = (random.randint(1,10000) % int(db.session.query(func.count(Words.id)).scalar()));
                current_app.logger.info("wrongMeaningId="+str(wrongMeaningId));
                wrongMeaning = Words.query.get(int(wrongMeaningId));
            current_app.logger.info("wrongMeaning word:"+wrongMeaning.word);
            questionaire[key] = wrongMeaning.meaning.split("~~")[1];
        i = i+1;
    session['questionaire'] = questionaire;
    current_app.logger.info("Adding questionaire to session "+ str(questionaire));
    return render_template('home/quiz.html',questionaire=questionaire);
    