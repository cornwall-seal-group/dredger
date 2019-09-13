from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
import os
import config

IMAGES_FOLDER = config.IMAGES_FOLDER
ENDPOINT = config.ENDPOINT
TRAINING_KEY = config.TRAINING_KEY


def create_classifier_model(tag):
    trainer = CustomVisionTrainingClient(TRAINING_KEY, endpoint=ENDPOINT)

    # Create a new project
    project_name = "Classifier: " + tag
    print ("Creating project... " + project_name)
    project = trainer.create_project(project_name)

    tags = {}
    image_list = []

    for subdir, dirs in os.walk(IMAGES_FOLDER):

        # See whether we have the tag folder for the seal
        for subdirname in dirs:
            seal_name = subdirname
            print seal_name

            if seal_name == 'pjf348':

                tag_path = os.path.join(subdir, tag)

                if os.path.isdir(tag_path):
                    tags[seal_name] = trainer.create_tag(project.id, seal_name)

                    for file in os.listdir(tag_path):
                        image_path = os.path.join(tag_path, file)
                        with open(image_path, "rb") as image_contents:
                            print image_path

                            image_list.append(ImageFileCreateEntry(
                                name=file, contents=image_contents.read(), tag_ids=[tags[seal_name].id]))

                        # batch the requests
                        if len(image_list) == 60:
                            send_images(trainer, project, image_list)

                            image_list = []

    # send last images not hitting the 60 limit
    send_images(trainer, project, image_list)


def send_images(trainer, project, image_list):
    trainer.create_images_from_files(project.id, images=image_list)
