# Audio2Text
Audio-to-text conversion system

## Deployment with Docker
### Clone the repository
```sh
$ git clone https://github.com/maxnest0x0/audio2text.git
$ cd audio2text
```

### Build the image
Provide your [Hugging Face access token](https://hf.co/settings/tokens) as a build argument.
It is required to download the pyannote model.
Avoid publishing the image as it will contain your token.
```sh
$ docker build --tag audio2text --build-arg AUTH_TOKEN=token .
```

### Run the container
This will start the service at http://localhost:8000/.
CUDA will be used if a compatible GPU and drivers are detected, otherwise it will fall back to CPU.
Note that about 6 GB of VRAM is required to run the Whisper turbo model.
```sh
$ docker run --tty --gpus all --publish 8000:8000 audio2text
```

## Usage
### Web page
For PC and mobile users we host the web page at https://8000-maxnest0x0-audio2text-zz67jo9ycnb.ws-eu120.gitpod.io/.
Note that we are using CPU, as the GPU servers are very expensive nowadays, so the model will work slowly.

### API
For developers we provide an API endpoint.
API documentation is available via [Swagger UI](https://8000-maxnest0x0-audio2text-zz67jo9ycnb.ws-eu120.gitpod.io/docs) and [Redoc](https://8000-maxnest0x0-audio2text-zz67jo9ycnb.ws-eu120.gitpod.io/redoc).

## Screencast

https://github.com/user-attachments/assets/7af34599-c1b3-40d2-b763-d1da1f6e5277
