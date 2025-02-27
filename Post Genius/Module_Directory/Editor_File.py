import os
import base64
from io import BytesIO
import shutil
import re
from typing import Optional, List, Tuple, Union
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings

#------------------------------------------------(ImageMagick)----------------------------------------------------------
# ImageMagick'in taşınabilir (portable) sürümünü belirle
script_directory = os.path.dirname(os.path.abspath(__file__))  # Bu dosyanın bulunduğu dizin
imagemagick_path = os.path.join(script_directory, "ImageMagick-7.1.1-Q16-HDRI", "magick.exe")

# Eğer ImageMagick taşınabilir sürümü burada mevcutsa, MoviePy'ye bildir
if os.path.exists(imagemagick_path):
    change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})
else:
    raise FileNotFoundError("⚠️ Uyarı: ImageMagick bulunamadı! Program düzgün çalışmayabilir.")
#-----------------------------------------------------------------------------------------------------------------------

#------------------------------------------------(CLASSES)--------------------------------------------------------------
class TEXT_CLASS(object):
    def __init__(self,audio_clip: AudioFileClip,image_clip: ImageClip):
        self.audio_clip = audio_clip
        self.image_clip = image_clip

    @staticmethod
    def split_text_by_punctuation(text):
        sentences = re.split(r'([.!?])', text)
        sentences = ["".join(sentences[i:i + 2]).strip() for i in range(0, len(sentences) - 1, 2)]
        return sentences

    @staticmethod
    def calculate_sentence_durations(audio_duration, num_sentences):
        avg_duration = audio_duration / max(num_sentences, 1)
        return [avg_duration] * num_sentences

    def fixed_text(self, text: Optional[str] = None, text_settings: Optional[List[Union[int, str, float]]] = None, bg_color: Tuple = (255, 255, 255), pos: Tuple = (0, 0)):
        if text is None:
            text = "Metin girmediniz!"
        if text_settings is None:
            text_settings = [40, 'black', 1.0]

        txt_clip = TextClip(
            text,
            fontsize=text_settings[0],
            color=text_settings[1],
            method='label'
        ).set_duration(self.audio_clip.duration)

        txt_w, txt_h = txt_clip.size
        padding = 5

        bg_clip = ColorClip(
            size=(txt_w + 2 * padding, txt_h + 2 * padding),
            color=bg_color
        ).set_duration(self.audio_clip.duration).set_opacity(text_settings[2])

        composite_clip = CompositeVideoClip(
            [bg_clip, txt_clip.set_position("center")],
            size=(txt_w + 2 * padding, txt_h + 2 * padding)
        ).set_duration(self.audio_clip.duration)

        composite_clip = composite_clip.set_position(pos)

        return composite_clip

    def subtitle_text_processing(self, text: Optional[str] = None, text_settings: Optional[List[Union[int, str, float]]] = None, bg_color: Tuple = (255, 255, 255), pos: Optional[Tuple[Union[int, int]]] = None):
        if text is None:
            text = "Alt yazı için text değeri giriniz!"
        if text_settings is None:
            text_settings = [20, 'white', 0.5]

        sentences = self.split_text_by_punctuation(text)
        durations = self.calculate_sentence_durations(self.audio_clip.duration, len(sentences))

        text_clips = []
        start_time = 0
        max_allowed_width = self.image_clip.w * 0.8
        for sentence, duration in zip(sentences, durations):
            txt_clip = TextClip(
                sentence,
                fontsize=text_settings[0],
                color=text_settings[1],
                method='label'
            ).set_duration(duration)

            txt_w, txt_h = txt_clip.size
            padding = 10
            total_width = txt_w + 2 * padding
            scale_factor = 1.0
            if total_width > max_allowed_width:
                scale_factor = max_allowed_width / total_width
                txt_clip = txt_clip.resize(scale_factor)
                txt_w, txt_h = txt_clip.size

            bg_clip = ColorClip(
                size=(txt_w + 2 * padding, txt_h + 2 * padding),
                color=bg_color
            ).set_duration(duration).set_opacity(text_settings[2])

            txt_with_bg = CompositeVideoClip(
                [bg_clip, txt_clip.set_position("center")],
                size=(txt_w + 2 * padding, txt_h + 2 * padding)
            ).set_duration(duration)

            img_w, img_h = self.image_clip.size
            margin = 20
            if pos is None:
                pos = ((img_w - (txt_w + 2 * padding)) / 2, img_h - (txt_h + 2 * padding) - margin)
            txt_with_bg = txt_with_bg.set_position(pos).set_start(start_time)

            text_clips.append(txt_with_bg)
            start_time += duration

        return text_clips


def run(image_path: str, audio_path: str, text: str) -> bytes:
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path).set_duration(audio_clip.duration)

    video_texts = TEXT_CLASS(audio_clip, image_clip)

    # Altyazı metinlerini oluşturuyoruz
    subtitle_clips = video_texts.subtitle_text_processing(text, [50, 'black', 0.7], (255, 255, 255))

    # "Post Genius" metnini sol üst köşeye eklemek için fixed_text fonksiyonunu kullanıyoruz
    fixed_text_clip = video_texts.fixed_text("Post Genius", [20, 'white', 0.5], (153, 50, 204), (10, 10))

    # Oluşturduğumuz klipleri videoya ekliyoruz
    video = CompositeVideoClip([image_clip] + subtitle_clips + [fixed_text_clip]).set_audio(audio_clip)

    temp_video_path = "temp_video.mp4"
    video.write_videofile(temp_video_path, fps=24, codec="libx264", audio_codec="aac")

    return temp_video_path