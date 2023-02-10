# Getting the Base Image
FROM alpine:latest

# Adding layers to the base image
RUN apk add --no-cache python3-dev \
    py3-pip

RUN apk add gcc musl-dev mariadb-connector-c-dev


# making the working directory (/expense_login_App will be the ROOT directory)
WORKDIR /expense_login_App

# Copy all the content from source <local system files> to destination <docker_app directory>
COPY . /expense_login_App/

# Run this to install dependencies 
RUN pip install -r requirements.txt

EXPOSE 5000

# Running this 
ENTRYPOINT ["python"] 

CMD ["./app.py"]


 
