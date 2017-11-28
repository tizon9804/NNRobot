# Use an official Python runtime as a parent image
FROM node:carbon

# Set the working directory to /app
WORKDIR /robotweb

# Copy the current directory contents into the container at /app
ADD . /robotweb

COPY package*.json ./

RUN npm install 
RUN npm install express-handlebars
RUN npm install mysql
#--only=production

# Make port 80 available to the world outside this container
EXPOSE 3000

# Run app.py when the container launches
CMD ["npm", "start"]
