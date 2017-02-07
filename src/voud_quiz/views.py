from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import *
from .forms import QuestionForm
from .models import *
import random

class QuizListView(ListView):
	model=Quiz

	def get_queryset(self):
		queryset=super(QuizListView,self).get_queryset()
		return queryset

class QuizDetailView(DetailView):
	model=Quiz
	slug_field='url'

	def get(self,request,*args,**kwargs):
		self.object=self.get_object()

		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

class QuizTake(FormView):
	form_class=QuestionForm
	template_name='question.html'

	def dispatch(self,request,*args,**kwargs):
		self.quiz=get_object_or_404(Quiz,url=self.kwargs['quiz_name'])
		self.sitting = self.anon_load_sitting()
		if self.sitting is False:
			return render(request,'single_complete.html')
		return super(QuizTake,self).dispatch(request,*args, **kwargs)

	def get_form(self, form_class=QuestionForm):
		self.question=self.anon_next_question()
		self.progress=self.anon_sitting_progress()


		return form_class(**self.get_form_kwargs())

	def get_form_kwargs(self):
		kwargs=super(QuizTake,self).get_form_kwargs()

		return dict(kwargs,question=self.question)
	def form_valid(self,form):
		self.form_valid_anon(form)
		if not self.request.session[self.quiz.anon_q_list()]:
			return self.final_result_anon()
		self.request.POST={}
		return super(QuizTake,self).get(self,self.request)

	def get_context_data(self,**kwargs):
		context=super(QuizTake,self).get_context_data(**kwargs)
		context['question']=self.question
		context['quiz']=self.quiz
		if hasattr(self,'previous'):
			context['previous']=self.previous
		if hasattr(self,'progress'):
			context['progress']=self.progress
		return context

	def anon_load_sitting(self):
		if self.quiz.anon_q_list() in self.request.session:
			return self.request.session[self.quiz.anon_q_list()]
		else:
			return self.new_anon_quiz_session()

	def new_anon_quiz_session(self):
		self.request.session.flush()
		self.request.session.set_expiry(259200)
		questions = self.quiz.get_questions()
		question_list=[question.id for question in questions]
		if self.quiz.random_order is True:
			random.shuffle(question_list)

		self.request.session[self.quiz.anon_score_id()]=0
		self.request.session[self.quiz.anon_q_list()]=question_list
		self.request.session[self.quiz.anon_q_data()]=dict(
			incorrect_questions=[],
			order=question_list,
			)
		return self.request.session[self.quiz.anon_q_list()]

	def anon_next_question(self):
		next_question_id = self.request.session[self.quiz.anon_q_list()][0]
		return Question.objects.get_subclass(id=next_question_id)

	def anon_sitting_progress(self):
		total=len(self.request.session[self.quiz.anon_q_data()]['order'])
		answered = total - len(self.request.session[self.quiz.anon_q_list()])
		return (answered,total)

	def form_valid_anon(self,form):
		guess = form.cleaned_data['answers']
		score_to = self.question.get_score(guess)
		#добавить очки
		if score_to==2:
			self.request.session[self.quiz.anon_score_id()]+=1
		else:
			self.request.session[self.quiz.anon_q_data()]['incorrect_questions'].append(self.question.id)

		self.anon_session_score(self.request.session, score_to,2)

		self.previous={}
		if self.quiz.answers_at_end is True:
			self.previous={
				'previous_answers':guess,
				'previous_outcome':score_to,
				'previous_question':self.question,
				'answers':self.question.get_answers(),
				'question_type':{self.question.__class__.__name__:True}
			}
		
		print(self.previous)
		self.request.session[self.quiz.anon_q_list()]=self.request.session[self.quiz.anon_q_list()][1:]

	def final_result_anon(self):
		score = self.request.session[self.quiz.anon_score_id()]
		q_order = self.request.session[self.quiz.anon_q_data()]['order']
		session, session_possible = self.anon_session_score(self.request.session)
		
		if score is 0:
			score = "0"
		results={
			'score':score,
			'session':session,
			'possible':session_possible,
			
		}

		del self.request.session[self.quiz.anon_q_list()]
		
		if self.quiz.answers_at_end:
			results['questions']=sorted(
				self.quiz.question_set.filter(id__in=q_order).select_subclasses(),
				key=lambda q: q_order.index(q.id)
				)
			results['incorrect_questions']=(
				self.request.session[self.quiz.anon_q_data()]['incorrect_questions']
				)
		
		results['previous']=self.previous
		
		del self.request.session[self.quiz.anon_q_data()]
		

		return render(self.request,'result.html',results)

	def anon_session_score(self, session,to_add=0, possible=0):
		if "session_score" not in session:
			session["session_score"],session["session_score_possible"] = 0,0
		if possible>0:
			session["session_score"]+=to_add
			session["session_score_possible"]+=possible

		return session["session_score"], session["session_score_possible"]




