from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
import os
import config
from PIL import Image
from math import ceil
import io

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
    required_image_count = 50
    folders_to_exclude = ['albums', 'no-ids', 'zipfiles']

    for seal_name in os.listdir(IMAGES_FOLDER):

        if seal_name not in folders_to_exclude:
            print 'About to process: ' + seal_name

            tag_path = os.path.join(IMAGES_FOLDER, seal_name, tag)

            if os.path.isdir(tag_path):

                tagpath, tagdirs, tagfiles = next(os.walk(tag_path))
                num_images_for_seal = len(tagfiles)

                print 'Number of images found: ' + str(num_images_for_seal)

                if num_images_for_seal > 2:

                    tags[seal_name] = trainer.create_tag(project.id, seal_name)

                    for file in os.listdir(tag_path):
                        num_rotations_per_image = int(
                            ceil(required_image_count / num_images_for_seal))

                        rotations_each_way = (int(
                            ceil(num_rotations_per_image / 2)) + 2)

                        image_path = os.path.join(tag_path, file)

                        for number in range(rotations_each_way):
                            pil_image = Image.open(image_path)
                            rotated = pil_image.rotate(number)

                            img_byte_arr = io.BytesIO()
                            rotated.save(img_byte_arr, format='PNG')
                            img_byte_arr = img_byte_arr.getvalue()

                            image_list.append(ImageFileCreateEntry(
                                name=file, contents=img_byte_arr, tag_ids=[tags[seal_name].id]))

                            # batch the requests
                            if len(image_list) == 60:
                                send_images(trainer, project, image_list)

                                image_list = []

                        for cc_number in range(359-rotations_each_way, 360):
                            pil_image = Image.open(image_path)
                            rotated = pil_image.rotate(cc_number)

                            img_byte_arr = io.BytesIO()
                            rotated.save(img_byte_arr, format='PNG')
                            img_byte_arr = img_byte_arr.getvalue()

                            image_list.append(ImageFileCreateEntry(
                                name=file, contents=img_byte_arr, tag_ids=[tags[seal_name].id]))

                            # batch the requests
                            if len(image_list) == 60:
                                send_images(trainer, project, image_list)

                                image_list = []

    # send last images not hitting the 60 limit
    send_images(trainer, project, image_list)


def send_images(trainer, project, image_list):
    trainer.create_images_from_files(project.id, images=image_list)
