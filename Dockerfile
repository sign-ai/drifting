# This is the final stage, anything here will be preserved in the final container image.
FROM python:3.9

# Set the current working directory to /code.
WORKDIR /code

# Install the package dependencies in the generated requirements.txt file.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app directory to the /code directory.
COPY ./app /code/app

# Run the drifting command
CMD ["drifting", "start", "--host", "0.0.0.0", "--port", "80", "detectors/"]
