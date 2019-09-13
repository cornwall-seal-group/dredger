from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
import os
import config
from PIL import Image

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
    required_image_count = 4

    for seal_name in os.listdir(IMAGES_FOLDER):

        print seal_name

        if seal_name == 'pjf348':

            tag_path = os.path.join(seal_name, tag)

            if os.path.isdir(tag_path):
                tags[seal_name] = trainer.create_tag(project.id, seal_name)

                num_images_for_seal = len(
                    [name for name in os.listdir(tag_path) if os.path.isfile(name)])
                for file in os.listdir(tag_path):
                    num_rotations_per_image = int(
                        ceil(required_image_count / num_images_for_seal))

                    rotations_each_way = int(
                        ceil(num_rotations_per_image / 2)) + 1

                    image_path = os.path.join(tag_path, file)
                    # with open(image_path, "rb") as image_contents:
                    #    print image_path

                    for number in range(rotations_each_way):
                        pil_image = Image.open(image_path)
                        rotated = pil_image.rotate(number)

                        image_list.append(ImageFileCreateEntry(
                            name=file, contents=rotated, tag_ids=[tags[seal_name].id]))

                        # batch the requests
                        if len(image_list) == 60:
                            #send_images(trainer, project, image_list)

                            image_list = []

    # send last images not hitting the 60 limit
    #send_images(trainer, project, image_list)


def send_images(trainer, project, image_list):
    trainer.create_images_from_files(project.id, images=image_list)
