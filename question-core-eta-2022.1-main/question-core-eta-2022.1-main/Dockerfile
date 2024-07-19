FROM registry.gitlab.com/kls6771243/question-core-eta-2022.1:dependencies

COPY . .

RUN mkdir -p assets/static \
  && python manage.py collectstatic --noinput

CMD ["python","-u", "production-server.py"]
