import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
# model = source of truth for your data
# contains essential fields and behaviors of the data

#using: https://docs.djangoproject.com/en/1.8/intro/tutorial01/
#question = has a question and pub date
#choice = text of choice, vote tally, and also is tied to a question

#models.Model = subclasses from Django

#this creates a database schema (CREATE TABLE statements) for this app
#create a python database-access API for accessing the Question and Choice objects

class Question(models.Model):
	def __str__(self):
		return self.question_text
	def was_published_recently(self): #returns true or false
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now #was it published between yesterday and today?

	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'
	question_text = models.CharField(max_length=200)  #CharField -> data type
	pub_date = models.DateTimeField('date published') #1st argument is for human-readable name

class Choice(models.Model):
	def __str__(self):
		return self.choice_text
	question = models.ForeignKey(Question) #foreign key -> associates choice w/ question, remember those database days?
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

