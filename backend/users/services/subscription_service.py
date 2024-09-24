from backend.users.models import Subscribe


class SubscriptionService:
    def __init__(self, user):
        self.user = user

    def _create_subscription(self, author):
        if self.user.subscribed.filter(author=author).exists():
            raise ValueError("Вы уже подписаны на этого автора.")
        return Subscribe.objects.create(user=self.user, author=author)

    def _delete_subscription(self, author):
        subscription = self.user.subscribed.filter(author=author).first()
        if not subscription:
            raise ValueError("Подписка не найдена.")
        subscription.delete()
        return subscription
