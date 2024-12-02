from celery import Celery, Task
from flask import Flask


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
            beat_schedule={
                "post_thought_every_hour": {
                    "task": "post_thought",
                    "schedule": 3000
                },
                "post_channel_casts_every_2_hours": {
                    "task": "post_channel_casts",
                    "schedule": 7200
                },
                "post_thought_about_feed_every_1_5_hours": {
                    "task": "post_thought_about_feed",
                    "schedule": 5400
                },
            },
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app
