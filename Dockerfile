FROM python:3

LABEL maintainer="Jonathon Taylor"

ENV AWS_ACCESS_KEY_ID="" \
    AWS_SECRET_ACCESS_KEY="" \
    AWS_HOSTED_ZONE_ID="" \
    AWS_A_RECORD_NAME="name.domain.com." \
    SLEEP_SEC='360'

ADD r53dyn/r53dyn.py /
ADD r53dyn/helpers.py /
ADD r53dyn/template_A.json /
ADD requirements.txt /
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements.txt
CMD [ "python","-u", "./r53dyn.py" ]