import hashlib
from django.db import models

class App(models.Model):    
    name = models.TextField(max_length=200)
    registerd_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    @property
    def api_key(self):
        # Generate the hash value of self.id
        hash_object = hashlib.sha256(str(self.id).encode())
        return hash_object.hexdigest()



class Question(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)    
    text = models.TextField()
    


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Question_detail", kwargs={"pk": self.pk})



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    
    @classmethod
    def total_votes(cls):
        return cls.objects.aggregate(total_votes=models.Sum('votes'))['total_votes'] or 0


    @property
    def percentage_of_votes(self):
        total_votes = self.question.choice_set.aggregate(total_votes=models.Sum('votes'))['total_votes'] or 0
        if total_votes == 0:
            return 0
        else:
            percentage = (self.votes / total_votes) * 100
            return round(percentage, 1)  



# class CustomUser(models.Model):
#     user_id = models.IntegerField(default=0)
#     app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="users")
    
class VotingRecord(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="voting_records")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="voting_records")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="voting_records")
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.app.name
    

