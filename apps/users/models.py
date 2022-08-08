from django.db import models



# class Friend(models.Model):
#     """
#     Friends models
#     """
#     user = models.ForeignKey(
#         AuthUser, on_delete=models.CASCADE, related_name='user'
#     )
#     friend = models.ForeignKey(
#         AuthUser, on_delete=models.CASCADE, related_name='friends'
#     )

#     def __str__(self):
#         return f'{self.friend} is friend with {self.user}'
    

# class SocialLinks(models.Model):
#     """
#     Social links belong to AuthUser
#     """
#     user = models.ForeignKey(
#         AuthUser, on_delete=models.CASCADE, related_name='social_links'
#     )
#     link = models.URLField(max_length=100)

#     def __str__(self):
#         return f'{self.user}'