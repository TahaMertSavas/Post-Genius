import OpenAI_File
import DatabaseOperations_File
import ElevenLabs_File
import Editor_File
import sys
import os
import base64
import shutil
#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------(Create folders)--------------------------------------------------------
script_directory = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.dirname(script_directory)

audio_folder_path = os.path.join(project_folder, "Audio Files")
os.makedirs(audio_folder_path, exist_ok=True)

image_folder_path = os.path.join(project_folder, "Image Files")
os.makedirs(image_folder_path, exist_ok=True)

edited_folder_path = os.path.join(project_folder, "Edited Files")
os.makedirs(edited_folder_path, exist_ok=True)
#-----------------------------------------------------------------------------------------------------------------------

text = str(input("İçerik fikri giriniz... :  "))
#-----------------------------------------------------------------------------------------------------------------------
OpenAI_File_output = OpenAI_File.run(text,[0,5])
image_file_path = os.path.join(image_folder_path, "output_image.png")
with open(image_file_path, "wb") as file:
    file.write(OpenAI_File_output[-1])
#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
ElevenLabs_File_output = ElevenLabs_File.run(OpenAI_File_output[0])
audio_file_path = os.path.join(audio_folder_path, "output_audio.mp3")
with open(audio_file_path, "wb") as f:
    f.write(base64.b64decode(ElevenLabs_File_output))
#-----------------------------------------------------------------------------------------------------------------------

#----------------------------------------------- ------------------------------------------------------------------------
Editor_File_output = Editor_File.run(image_file_path, audio_file_path, OpenAI_File_output[0])
edited_file_path = os.path.join(edited_folder_path, "output_edit.mp4")
shutil.move(Editor_File_output, edited_file_path)
#-----------------------------------------------------------------------------------------------------------------------
