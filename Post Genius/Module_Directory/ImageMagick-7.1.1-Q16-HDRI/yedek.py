import os
import base64
from io import BytesIO
import shutil
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

# 🛠️ ImageMagick'in taşınabilir (portable) sürümünü belirle
script_directory = os.path.dirname(os.path.abspath(__file__))  # Bu dosyanın bulunduğu dizin
imagemagick_path = os.path.join(script_directory, "ImageMagick-7.1.1-Q16-HDRI", "magick.exe")

# Eğer ImageMagick taşınabilir sürümü burada mevcutsa, MoviePy'ye bildir
if os.path.exists(imagemagick_path):
    change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})
else:
    raise FileNotFoundError("⚠️ Uyarı: ImageMagick bulunamadı! Program düzgün çalışmayabilir.")

def split_text_by_punctuation(text):
    """
    Noktalama işaretlerine göre metni bölerek cümleleri oluşturur.
    """
    import re
    sentences = re.split(r'([.!?])', text)  # Nokta, ünlem ve soru işaretine göre böl
    sentences = ["".join(sentences[i:i+2]).strip() for i in range(0, len(sentences)-1, 2)]
    return sentences

def calculate_sentence_durations(audio_duration, num_sentences):
    """
    Her cümle için yaklaşık süreyi hesaplar.
    """
    avg_duration = audio_duration / max(num_sentences, 1)
    return [avg_duration] * num_sentences

def run(image_path: str, audio_path: str, text: str) -> bytes:
    # 🎬 Video bileşenlerini oluştur
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path).set_duration(audio_clip.duration)

    # 📝 Metni cümlelere böl
    sentences = split_text_by_punctuation(text)
    durations = calculate_sentence_durations(audio_clip.duration, len(sentences))

    # 📝 Metin kliplerini oluştur
    text_clips = []
    start_time = 0
    for sentence, duration in zip(sentences, durations):
        # Metin klibini oluştururken genişliği sınırlıyoruz, yüksekliği otomatik ayarlansın
        txt_clip = TextClip(
            sentence,
            fontsize=50,
            color='white',
            method='caption',
            align='center',
            size=(int(image_clip.w * 0.8), None)  # Genişliği görüntünün %80'i, yükseklik otomatik
        )
        txt_clip = txt_clip.set_duration(duration).set_start(start_time)

        # Metin klibinin boyutlarını alalım
        txt_w, txt_h = txt_clip.size
        img_w, img_h = image_clip.size
        margin = 20  # Alt kenardan 20 piksel boşluk

        # Metni ekranın alt ortasına yerleştiriyoruz
        txt_clip = txt_clip.set_position(((img_w - txt_w) / 2, img_h - txt_h - margin))
        text_clips.append(txt_clip)
        start_time += duration  # Yeni başlangıç süresini ayarla

    # 🎥 Videoyu oluştur
    video = CompositeVideoClip([image_clip] + text_clips).set_audio(audio_clip)

    # 📂 Geçici bir dosyaya video kaydet
    temp_video_path = "temp_video.mp4"
    video.write_videofile(temp_video_path, fps=24, codec="libx264", audio_codec="aac")

    return temp_video_path








#-----------------------------------------------------------------------------------------------------------------------
script_directory = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.dirname(script_directory)
audio_folder_path = os.path.join(project_folder, "Audio Files")
image_folder_path = os.path.join(project_folder, "Image Files")
edited_folder_path = os.path.join(project_folder, "Edited Files")
image_file_path = os.path.join(image_folder_path, "output_image.png")
audio_file_path = os.path.join(audio_folder_path, "output_audio.mp3")

text = "Karanlık, insanlık tarihi boyunca merak edilmiş ve korkutmuştur. Ancak, onun içindeki sırları çözmek ve aydınlığa dönüştürmek de bizim elimizdedir. ık  ınlanma"
Editor_File_output = run(image_file_path, audio_file_path, text)
edited_file_path = os.path.join(edited_folder_path, "output_edit.mp4")
shutil.move(Editor_File_output, edited_file_path)
