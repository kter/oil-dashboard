FROM public.ecr.aws/lambda/python:3.12

COPY pyproject.toml ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir .

COPY src/ ${LAMBDA_TASK_ROOT}/

CMD ["handler.lambda_handler"]
