from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

# Register your models here.
from .models import Answer,Question,Quiz,Subject

class AnswerInline(admin.TabularInline):
	model=Answer

class QuizAdminForm(forms.ModelForm):
	class Meta:
		model = Quiz
		exclude=[]

	questions = forms.ModelMultipleChoiceField(
		queryset=Question.objects.all().select_subclasses(),
		required=False,
		widget=FilteredSelectMultiple(verbose_name="Вопросы",is_stacked=False))

	def __init__(self,*args,**kwargs):
		super(QuizAdminForm,self).__init__(*args,**kwargs)
		if self.instance.pk:
			self.fields['questions'].initial=\
			self.instance.question_set.all().select_subclasses()
	def save(self,commit=True):
		quiz=super(QuizAdminForm,self).save(commit=False)
		quiz.save()
		quiz.question_set=self.cleaned_data['questions']
		self.save_m2m()
		return quiz

class QuizAdmin(admin.ModelAdmin):
	form = QuizAdminForm
	list_display=['name','subject',]
	list_filter=['subject',]

class SubjectAdmin(admin.ModelAdmin):
	search_fields=['subject']

class QuestionAdmin(admin.ModelAdmin):
	list_display = ['content']
	
	fields=['content','figure','quiz','random_order']

	filter_horizontal=['quiz']
	inlines=[AnswerInline]

admin.site.register(Quiz,QuizAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Question,QuestionAdmin)

