from django.db import models
import re

from model_utils.managers import InheritanceManager
# Create your models here.

class Subject(models.Model):
	subject=models.CharField(max_length=250,unique=True, blank=False)
	class Meta:
		verbose_name="Предмет"
		verbose_name_plural = "Предметы"
	def __str__(self):
		return self.subject

class Quiz(models.Model):
	name=models.CharField(max_length=120,blank=False)
	url=models.SlugField(max_length=120,blank=False)
	subject=models.ForeignKey(Subject)
	random_order = models.BooleanField(blank=False,default=False)
	answers_at_end = models.BooleanField(blank=False,default=False)

	def save(self,force_insert=False, force_update=False, *args,**kwargs):
		self.url = re.sub(r'\s+','-',self.url).lower()

		self.url=''.join(letter for letter in self.url if letter.isalnum() or letter=='-')
		super(Quiz,self).save(force_insert,force_update,*args,**kwargs)
	class Meta:
		verbose_name="Тест"
		verbose_name_plural="Тесты"
	def __str__(self):
		return self.name

	def get_questions(self):
		return self.question_set.all().select_subclasses()

	def anon_score_id(self):
		return str(self.id)+"_score"

	def anon_q_list(self):
		return str(self.id)+"_q_list"
	def anon_q_data(self):
		return str(self.id)+"_data"



class Question(models.Model):
	quiz = models.ManyToManyField(Quiz,verbose_name=u"Тест",blank=True)
	
	figure = models.ImageField(upload_to='uploads/%Y/%m/%d',blank=True,null=True)
	content=models.CharField(max_length=1000,blank=False)
	random_order=models.BooleanField(blank=False,default=False)
	objects=InheritanceManager()

	class Meta:
		verbose_name="Вопрос"
		verbose_name_plural="Вопросы"
		
	def __str__(self):
		return self.content

	def get_score(self,guess):#сюда надо положить все выбранные варианты пользоватля
		all_answers=Answer.objects.filter(question=self)
		rights=0
		for q_answer in all_answers:
			if q_answer.correct is True:
				rights+=1
		corrects=0
		incorrects=0
		for guess_id in guess:
			answer = Answer.objects.get(id=int(guess_id))
			if answer.correct is True:
				corrects+=1
			else:
				incorrects+=1
		if corrects != 0:
			if (rights==corrects)and(incorrects==0):
				return 2
			elif (corrects==(rights-1))and(incorrects==0):
				return 1
			elif (rights==corrects)and(incorrects==1):
				return 1
			else:
				return 0
		else:
			return 0





	def random_answers(self,queryset):
		if self.random_order is True:
			return queryset.order_by('?')
		else:
			return queryset.order_by()
	def get_answers(self):
		return self.random_answers(Answer.objects.filter(question=self))
	def get_answers_list(self):
		return [(answer.id,answer.answer)for answer in 
		self.random_answers(Answer.objects.filter(question=self))]
	def answer_choice_to_string(self, guess):
		return Answer.objects.get(id=guess).answer




class Answer(models.Model):
	question=models.ForeignKey(Question, verbose_name="Вопрос")
	answer=models.CharField(max_length=1000,blank=False)
	correct=models.BooleanField(blank=False,default=False)
	def __str__(self):
		return self.answer

	class Meta:
		verbose_name="Ответ"
		verbose_name_plural="Ответы"

