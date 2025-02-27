from openai import OpenAI
import os
import base64
import re

#---------------------------------------------------(API KEY)-----------------------------------------------------------
api_key1 = "OPENAI API KEYINIZI GIRINIZ<->ENTER YOUR API KEY"
client = OpenAI(api_key = api_key1)
#-----------------------------------------------------------------------------------------------------------------------
size1 = "256x256"
size2 = "512x512"
size3 = "1024x1024"
size4 = "1024x1792"
size5 = "1792x1024"

model_1 = "gpt-3.5-turbo-instruct"
class OPENAI_CLASS(object):
    def __init__(self,model,content):
        self.model = model
        self.content = content

    def text_generator(self):
        try:
            completion = client.completions.create(
                model=self.model,
                prompt=self.content,
                max_tokens=1000,
                temperature=0.7,
            )
            response = completion.choices[0].text.strip()
            if '#' in response:
                response = response.split('#')[0].strip()
            #response = re.sub(r"#[A-Za-z0-9_]+|@[A-Za-z0-9_]+|<[^>]+>", "", response)

            return response

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def image_generator(self):
        response = client.images.generate(
            prompt=self.content,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )


        if response.data:
            image_b64 = response.data[0].b64_json
            return image_b64
        else:
            print("Görsel oluşturulamadı.")



    def output(self,func):
        if func == "text_generator":
            return self.text_generator()
        elif func == "image_generator":
            return self.image_generator()

def run(content_determinant_input, content_list):
    content = None
    metadata_entry = None
    outputs = []
    for content_no in content_list:
        if content_no == 0:  # İçerik
            content_description = (
                "'{0}'\n"
                "Bu konu, AI tarafından belirlenmiş bir sosyal medya paylaşım konusu. "
                "Görevin, bu konuya uygun, ilgi çekici ve özgün bir içerik oluşturmak. "
                "İçeriği şiir, motivasyon sözü, ders çıkarabileceğin bir hikaye veya pratik bir tavsiye şeklinde üretebilirsin. "
                "Lütfen, oluşturacağın metnin 25 kelimeyi aşmamasına dikkat et. "
                "Metnin içerisinde seslendirme programının okuyamayacağı tag gibi unsurlar bulunmamalı."
            )
            content = content_description.format(content_determinant_input)
        elif content_no == 1:  # Başlık
            metadata_description = (
                "'{0}'\n"
                "Bu metin, AI tarafından oluşturulmuş sosyal medya içeriğine dayanmaktadır. "
                "Lütfen, bu içerik için kısa, etkileyici ve öz bir başlık üret."
            )
            metadata_entry = metadata_description.format(content)
        elif content_no == 2:  # Açıklama
            metadata_description = (
                "'{0}'\n"
                "Bu metin, AI tarafından oluşturulmuş sosyal medya içeriğine dayanmaktadır. "
                "Görevin, bu içerik için içeriğin ana fikrini özetleyen kısa ve dikkat çekici bir açıklama oluşturmak."
            )
            metadata_entry = metadata_description.format(content)
        elif content_no == 3:  # Tag
            metadata_description = (
                "'{0}'\n"
                "Bu metin, AI tarafından oluşturulmuş sosyal medya içeriğine dayanmaktadır. "
                "Lütfen, içerikle doğrudan ilişkili uygun ve popüler etiketler (tag'ler) oluştur."
            )
            metadata_entry = metadata_description.format(content)
        elif content_no == 4:  # Video Prompt
            metadata_description = (
                "'{0}'\n"
                "Bu içerik, sosyal medyada paylaşılacak bir video için hazırlanmıştır. "
                "Lütfen, bu içerikle uyumlu, etkileyici ve sinematik bir 5 saniyelik video promptu yaz. "
                "Kullanılacak sahneleri, atmosferi, renkleri ve geçiş efektlerini belirt."
            )
            metadata_entry = metadata_description.format(content)
        elif content_no == 5:  # Image Prompt
            metadata_description = (
                "'{0}'\n"
                "Bu içerik, sosyal medyada paylaşılacak bir görsel için hazırlanmıştır. "
                "Lütfen, çekici, estetik ve kısa (1000 karakter altı) bir resim promptu yaz. "
                "Kompozisyon, renk paleti ve stil gibi temel detayları belirt."
            )
            metadata_entry = metadata_description.format(content)

        if content_no in [0]:
            content_generator = OPENAI_CLASS(model_1, content)
            outputs.append(content_generator.output("text_generator"))
            content = outputs[0]
        elif content_no in [1, 2, 3, 4, 5]:
            metadata_generator = OPENAI_CLASS(model_1, metadata_entry)
            prompt_text = metadata_generator.output("text_generator")
            if content_no == 5:
                # Prompt metnini 1000 karaktere kadar kısalt
                prompt_text = prompt_text[:1000]
                outputs.append(prompt_text)
                image_creator = OPENAI_CLASS(model_1, prompt_text)
                image_b64 = image_creator.output("image_generator")
                image_data = base64.b64decode(image_b64)
                outputs.append(image_data)
            else:
                outputs.append(prompt_text)
    return outputs
