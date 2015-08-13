import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question

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