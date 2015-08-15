import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.core.urlresolvers import reverse

# Create your tests here.

class QuestionMethodTests(TestCase): #create subclass
	def test_was_published_recently_with_future_question(self):
		""" 
		was_published_recently() should return False for questions whose pub date is in the future 
		"""

		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time) #creates a question w/ pubdate future
		self.assertEqual(future_question.was_published_recently(), False) #check output


	#adding more test methods to the same class

	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() should return False for questions whose pub_date is older than 1 day
		"""
		#note: we define the time variable here again, separate from other methods
		time = timezone.now()  - datetime.timedelta(days=30) #time =  30 days ago
		old_question = Question(pub_date=time) #create question published in the past
		self.assertEqual(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		question that has a pub date between now and 24 hours ago should return True
		""" 
		time = timezone.now() - datetime.timedelta(hours=1) #time is now 1 hour ago 
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)

def create_question(question_text, days):
	""" creates q with given 'question_text' published the given # of days offset to now (negative for 
	past published questions, positive for questions with a future pub date)
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
	def test_index_view_with_no_question(self):
		"""
		if no questions exist, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200) 
		self.assertContains(response, "No polls are available.") 
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_past_question(self):
		"""
		Questions with pub_date in the past shoudl be displayed on index page
		"""
		create_question(question_text="Past question", days=-30) #30 days ago from now
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question>']
		)

	def test_index_view_with_future_question(self):
		"""
		Questions with pub_date in future should NOT be displayed on index page
		"""
		create_question(question_text="Future question", days=30) #30 days in future
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.", #nothing should load 'successfully'
							status_code=200)
		self.assertQuerysetEqual(response.context['latest_question_list'], []) #should be empty

	def test_index_view_with_past_and_future_question(self):
		"""
		even if both past and future q's exist, only past questions should displayed
		"""
		create_question(question_text="Past question", days=-30)
		create_question(question_text="Future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question>']
		)

	def test_index_view_with_two_past_question(self): 
		"""
		the questions index page needs to display multiple questions.
		"""
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question 2.>', '<Question: Past question 1.>']
		)

class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_future_question(self):
		"""
		the detail view of a question w/ pub_date = future date should
		return 404
		"""
		future_question = create_question(question_text='Future question.', days=5)
		response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_past_question(self):
		"""
		the detail view of question with pubdate lte current should display q question_text
		"""
		past_question = create_question(question_text="Past question.", days=-5)
		response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
		self.assertContains(response, past_question.question_text, status_code=200) 
		#should contain question text and be a successful http request
